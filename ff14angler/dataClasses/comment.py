#! /usr/bin/env python3

import copy
import re

from dataclasses import dataclass
from datetime import datetime
from typing import List, Set

from bs4 import BeautifulSoup
from bs4.element import Tag


timestamp_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")
request_id_regex = re.compile(r"RID(\s+)?=(\s+)?(\d+);")


@dataclass(frozen=True)
class Comment:
    comment_author: str
    comment_text_original: str
    comment_text_translated: str
    comment_timestamp: datetime

    def __json__(self):
        _temp = self.__dict__
        _temp['comment_timestamp'] = str(self.comment_timestamp)
        return _temp

    @staticmethod
    async def _parse_author(info: Tag) -> str:
        text = info.text.strip()
        match = timestamp_regex.search(text)
        return text.replace(match[0], '').strip()

    @staticmethod
    async def _parse_timestamp(info: Tag) -> datetime:
        match = timestamp_regex.search(info.text.strip())
        return datetime.strptime(match[0], '%Y-%m-%d %H:%M:%S')

    @staticmethod
    async def _parse_text_original(soup: Tag) -> str:
        for tag in soup.find_all('span', {'class': 'comment_translate'}):  # type: Tag
            tag.decompose()

        return soup.text.strip()

    @staticmethod
    async def _parse_text_translated(soup: Tag) -> str:
        for tag in soup.find_all('span', {'class': 'comment_origin'}):  # type: Tag
            tag.decompose()

        return soup.text.strip()

    @staticmethod
    async def _parse_rid_from_soup(soup: BeautifulSoup) -> int:
        script_tag: Tag = soup.find('script', {'type': 'text/javascript'}, text=request_id_regex)
        return int(request_id_regex.search(str(script_tag)).groups()[2])

    @classmethod
    async def get_comment_from_comment_soup(cls, soup: Tag) -> 'Comment':
        info: Tag = soup.find('span', {'class': 'comment_info'})
        comment_author = await cls._parse_author(info)
        comment_timestamp = await cls._parse_timestamp(info)
        info.decompose()
        extracted = soup.extract()

        return cls(
            comment_author=comment_author,
            comment_text_original=await cls._parse_text_original(copy.copy(extracted)),
            comment_text_translated=await cls._parse_text_translated(soup),
            comment_timestamp=comment_timestamp
        )

    @staticmethod
    async def get_comments_from_angler_comment_section_soup(soup: BeautifulSoup) -> List['Comment']:
        comment_container: Tag = soup.find('div', {'class': 'comment_list'})
        comment_list_soup: List[Tag] = comment_container.find_all('div', {'class': 'comment'})

        temp_comment_list: Set[Comment] = set()

        for soup_comment in comment_list_soup:

            temp_comment_list.add(await Comment.get_comment_from_comment_soup(soup_comment))

        return list(temp_comment_list)
