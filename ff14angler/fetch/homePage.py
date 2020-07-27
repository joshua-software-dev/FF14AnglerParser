#! /usr/bin/env python3

import asyncio
import time

import lxml

from typing import Any, Awaitable, Dict, Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ..dataClasses.baitInfo import Bait, BaitInfo


class HomePage:

    # noinspection SpellCheckingInspection
    @staticmethod
    async def _dict_awaiter(key: str, value: Awaitable[Bait]) -> Tuple[str, Bait]:
        return key, await value

    @classmethod
    async def _parse_bait_list(cls, bait_parent: Tag):
        bait_holder: Dict[str, Awaitable[Bait]] = dict()

        for tag in sorted(bait_parent.find_all('option'), key=lambda x: int(x.attrs['value'])):  # type: Tag
            text: str = tag.text.strip()

            # S,N,L Spearfishing heads
            # Ha ha, SNL
            if text not in {'Select Bait', 'Small', 'Normal', 'Large'}:
                bait_holder[text] = Bait.get_bait_from_angler_name(text, int(tag.attrs['value']))

        BaitInfo.bait.update(
            {
                k: v for k, v in await asyncio.gather(
                    *(cls._dict_awaiter(key, task) for key, task in bait_holder.items())
                )
            }
        )

    @classmethod
    async def parse_homepage_data(cls, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, lxml.__name__)
        bait_parent: Tag = soup.find('select', {'name': 'bait'})
        fish_parent: Tag = soup.find('select', {'name': 'fish'})
        spot_parent: Tag = soup.find('select', {'name': 'spot'})

        await cls._parse_bait_list(bait_parent)

        fish_list: Dict[int, str] = {
            int(tag.attrs['value']): tag.text.strip() for tag in sorted(
                fish_parent.find_all('option'),
                key=lambda x: int(x.attrs['value'])
            ) if tag.text.strip() != 'Select Fish'
        }

        spot_list: Dict[int, str] = {
            int(tag.attrs['value']): tag.text.strip() for tag in sorted(
                spot_parent.find_all('option'),
                key=lambda x: int(x.attrs['value'])
            ) if tag.text.strip() != 'Select Location'
        }

        return {
            'bait': BaitInfo,
            'fish': fish_list,
            'spot': spot_list
        }

    @staticmethod
    async def check_is_truly_loaded(driver: WebDriver):
        while True:
            soup = BeautifulSoup(driver.page_source, lxml.__name__)
            bait_parent: Tag = soup.find('select', {'name': 'bait'})
            fish_parent: Tag = soup.find('select', {'name': 'fish'})
            if len(fish_parent.find_all('option')) > 100 and len(bait_parent.find_all('option')) > 50:
                return
            time.sleep(1)

    @classmethod
    async def collect_homepage_data(cls, driver: WebDriver) -> Dict[str, Dict[int, str]]:
        driver.get('https://en.ff14angler.com/')

        try:
            WebDriverWait(driver, 60).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, 'form_search')
                )
            )
        except TimeoutException:
            raise

        await cls.check_is_truly_loaded(driver)
        return await cls.parse_homepage_data(driver.page_source)
