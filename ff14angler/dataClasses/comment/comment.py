#! /usr/bin/env python3

import copy

import lxml  # type: ignore

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Set

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore

from ff14angler.constants.regex import timestamp_matcher_regex


@dataclass(frozen=True)
class Comment:
    comment_author: str
    comment_text_original: str
    comment_text_translated: str
    comment_timestamp: datetime

    @staticmethod
    async def _parse_author(info: Tag) -> str:
        text = info.text.strip()
        match = timestamp_matcher_regex.search(text)
        if match:
            return text.replace(match[0], '').strip()
        raise ValueError(f'Could not parse author from comment: {info}')

    @staticmethod
    async def _parse_timestamp(info: Tag) -> datetime:
        match = timestamp_matcher_regex.search(info.text.strip())
        if match:
            return datetime.strptime(match[0], '%Y-%m-%d %H:%M:%S')
        raise ValueError(f'Could not parse timestamp from comment: {info}')

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
    async def get_comment_from_angler_comment_json(cls, comment_json: Dict[str, Any]):
        comment_soup = BeautifulSoup(f'<html><div>{comment_json["comment"]}</div></html>', lxml.__name__)

        return cls(
            comment_author=BeautifulSoup(
                f'<html><div class="escape_name">{comment_json["nickname"]}</div></html>',
                lxml.__name__
            ).find('div', {'class': 'escape_name'}).text.strip(),
            comment_text_original=await cls._parse_text_original(copy.copy(comment_soup)),
            comment_text_translated=await cls._parse_text_translated(comment_soup),
            comment_timestamp=datetime.strptime(comment_json['date'], '%Y-%m-%d %H:%M:%S')
        )

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
