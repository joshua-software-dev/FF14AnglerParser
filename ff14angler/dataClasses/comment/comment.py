#! /usr/bin/env python3

import copy
import hashlib
import uuid

import lxml  # type: ignore

from dataclasses import dataclass, field
from datetime import datetime
from functools import cached_property
from typing import Any, Dict, List, Set, Tuple

from bs4 import BeautifulSoup  # type: ignore
from bs4.element import Tag  # type: ignore
from dataclasses_json import DataClassJsonMixin

from ff14angler.constants.regex import timestamp_matcher_regex


@dataclass(frozen=True)
class Comment(DataClassJsonMixin):
    comment_author: str
    comment_html: str
    comment_text_original: str
    comment_text_translated: str
    comment_timestamp: datetime = field(
        metadata={
            'dataclasses_json': {
                'decoder': datetime.fromisoformat,
                'encoder': datetime.isoformat
            }
        }
    )

    @cached_property
    def unique_id(self) -> uuid.UUID:
        comment_tuple: Tuple[str, str, str, str, str] = (
            self.comment_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            self.comment_author,
            self.comment_html,
            self.comment_text_original,
            self.comment_text_translated,
        )
        temp_md5 = hashlib.md5()
        temp_md5.update(f'{hash(comment_tuple)}'.encode('utf-8'))
        return uuid.UUID(temp_md5.hexdigest())

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
        comment_soup = BeautifulSoup(
            f'<html><div class="angler_parser">{comment_json["comment"]}</div></html>',
            lxml.__name__
        )

        # Remove iframe and script tags just in case
        for tag in comment_soup.find_all('iframe'):  # type: Tag
            tag.decompose()

        for tag in comment_soup.find_all('script'):  # type: Tag
            tag.decompose()

        return cls(
            comment_author=BeautifulSoup(
                f'<html><div class="escape_name">{comment_json["nickname"]}</div></html>',
                lxml.__name__
            ).find('div', {'class': 'escape_name'}).text.strip(),
            comment_html=comment_soup.find('div', {'class': 'angler_parser'}).decode_contents(),
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
            comment_html=str(extracted),
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
