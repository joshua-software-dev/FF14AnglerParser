#! /usr/bin/env python3

import copy
import re

from dataclasses import dataclass
from datetime import datetime

from bs4.element import Tag


timestamp_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


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

    @classmethod
    async def get_comment_from_soup(cls, soup: Tag) -> 'Comment':
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
