#! /usr/bin/env python3

import asyncio
import time

import lxml

from typing import Any, Awaitable, Dict, Tuple, TypeVar

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ..dataClasses.baitData import BaitData, BaitProvider
from ..dataClasses.fishData import FishData, FishProvider


T1 = TypeVar('T1')
T2 = TypeVar('T2')


class HomePage:

    # noinspection SpellCheckingInspection
    @staticmethod
    async def _dict_awaiter(key: T1, value: Awaitable[T2]) -> Tuple[T1, T2]:
        return key, await value

    @classmethod
    async def _parse_bait_list(cls, bait_parent: Tag):
        temp_bait_holder: Dict[str, Awaitable[BaitData]] = dict()

        for tag in sorted(bait_parent.find_all('option'), key=lambda x: int(x.attrs['value'])):  # type: Tag
            angler_bait_name: str = tag.text.strip()

            # S,N,L Spearfishing heads
            # Ha ha, SNL
            if angler_bait_name not in {'Select Bait', 'Small', 'Normal', 'Large'}:
                temp_bait_holder[angler_bait_name] = BaitProvider.get_bait_data_from_angler_name(angler_bait_name)

        BaitProvider.bait_holder.update(
            {
                k: v for k, v in await asyncio.gather(
                    *(cls._dict_awaiter(key, task) for key, task in temp_bait_holder.items())
                )
            }
        )

    @classmethod
    async def _parse_fish_list(cls, fish_parent: Tag):
        temp_fish_holder: Dict[str, Awaitable[FishData]] = dict()

        for tag in sorted(fish_parent.find_all('option'), key=lambda x: int(x.attrs['value'])):
            angler_fish_name: str = tag.text.strip()
            angler_fish_id: int = int(tag.attrs['value'])

            if angler_fish_name != 'Select Fish':
                temp_fish_holder[angler_fish_name] = FishProvider.get_fish_data_from_angler_name(
                    angler_fish_name,
                    angler_fish_id
                )

        FishProvider.fish_holder.update(
            {
                k: v for k, v in await asyncio.gather(
                    *(cls._dict_awaiter(key, task) for key, task in temp_fish_holder.items())
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
        await cls._parse_fish_list(fish_parent)

        spot_list: Dict[int, str] = {
            int(tag.attrs['value']): tag.text.strip() for tag in sorted(
                spot_parent.find_all('option'),
                key=lambda x: int(x.attrs['value'])
            ) if tag.text.strip() != 'Select Location'
        }

        return {
            'bait': BaitProvider,
            'fish': FishProvider,
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
        angler_url: str = 'https://en.ff14angler.com/'
        print(f'Scraping page: {angler_url}')
        driver.get(angler_url)

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
