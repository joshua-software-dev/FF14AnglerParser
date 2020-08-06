#! /usr/bin/env python3

import json
import urllib.parse

import lxml  # type: ignore

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

from bs4 import BeautifulSoup  # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore

from ff14angler.constants.regex import non_number_replacement_regex
from ff14angler.constants.values import ANGLER_BASE_URL
from ff14angler.dataClasses.comment.comment import Comment


comment_metadata_javascript = """\
comment_element = document.querySelector('.comment_list');
comment_type = comment_element.attributes[1].value;
comment_item = comment_element.attributes[2].value;
for (const small_tag of document.querySelectorAll('.small')) {
    if (small_tag.previousElementSibling.innerText == 'Comments')
    {
        return [RID, comment_type, comment_item, small_tag.innerText];
    }
}"""


@dataclass
class CommentSection:
    comments: List[Comment]
    comment_fetch_timestamp: datetime

    def __json__(self):
        temp = self.__dict__.copy()
        temp['comment_fetch_timestamp'] = self.comment_fetch_timestamp.isoformat()
        return temp

    @classmethod
    async def _get_request_metadata_from_web_driver(cls, driver: WebDriver) -> Tuple[int, int, int, int]:
        response: Tuple[int, str, str, str] = driver.execute_script(comment_metadata_javascript)
        request_id: int = response[0]
        type_id: int = int(response[1])
        item_id: int = int(response[2])
        max_comments: int = int(non_number_replacement_regex.sub(repl='', string=response[3]) or '0')

        return request_id, type_id, item_id, max_comments

    @classmethod
    async def parse_comment_section(cls, comment_list: List[Dict[str, Any]]) -> 'CommentSection':
        parsed_comment_list: List[Comment] = []
        for comment_json in comment_list:
            parsed_comment_list.append(await Comment.get_comment_from_angler_comment_json(comment_json))

        return cls(parsed_comment_list, datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc))

    @classmethod
    async def get_comment_section_from_web_driver(cls, driver: WebDriver) -> 'CommentSection':
        offset: int = 0
        comment_list: List[Dict[str, Any]] = []
        request_id, type_id, item_id, max_comments = await cls._get_request_metadata_from_web_driver(driver)

        while max_comments > 0:
            request_url: str = urllib.parse.urljoin(
                ANGLER_BASE_URL,
                '/comment.php?rid={}{}&limit=1000&type={}&item={}'.format(
                    request_id,
                    f'&offset={offset}' if offset > 0 else '',
                    type_id,
                    item_id
                )
            )

            print(f'Scraping comment URL: {request_url}')
            driver.get(request_url)

            if soup := BeautifulSoup(driver.page_source, lxml.__name__).find('pre'):
                if response := json.loads(soup.text.strip()):
                    comment_list += response['comment']
                    offset += 1000
                    if len(comment_list) < max_comments:
                        continue
            else:
                raise ValueError('No JSON response from server for comments.')
            break

        return await cls.parse_comment_section(comment_list=comment_list)
