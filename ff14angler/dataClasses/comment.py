#! /usr/bin/env python3

import copy
import re

from dataclasses import dataclass
from datetime import datetime

from bs4.element import Tag


timestamp_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")


@dataclass
class Comment:
    commenter: str = None
    text_original: str = None
    text_translated: str = None
    timestamp: datetime = None

    def __json__(self):
        _temp = self.__dict__
        _temp['timestamp'] = str(self.timestamp)
        return _temp

    @staticmethod
    def _parse_commenter(info: Tag) -> str:
        text = info.text.strip()
        match = timestamp_regex.search(text)
        return text.replace(match[0], '').strip()

    @staticmethod
    def _parse_timestamp(info: Tag) -> datetime:
        match = timestamp_regex.search(info.text.strip())
        return datetime.strptime(match[0], '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _parse_text_original(soup: Tag) -> str:
        for tag in soup.find_all('span', {'class': 'comment_translate'}):  # type: Tag
            tag.decompose()

        return soup.text.strip()

    @staticmethod
    def _parse_text_translated(soup: Tag) -> str:
        for tag in soup.find_all('span', {'class': 'comment_origin'}):  # type: Tag
            tag.decompose()

        return soup.text.strip()

    @classmethod
    def get_comment_from_soup(cls, soup: Tag) -> 'Comment':
        info: Tag = soup.find('span', {'class': 'comment_info'})

        comment = cls()
        comment.commenter = cls._parse_commenter(info)
        comment.timestamp = cls._parse_timestamp(info)

        info.decompose()
        extracted = soup.extract()
        comment.text_original = cls._parse_text_original(copy.copy(extracted))
        comment.text_translated = cls._parse_text_translated(soup)

        return comment


