#! /usr/bin/env python3

import asyncio
import time

import lxml

from typing import Any, Awaitable, Dict, List, Tuple, TypeVar

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from ff14angler.dataClasses.bait.baitProvider import Bait, BaitProvider
from ff14angler.dataClasses.fish.fishProvider import Fish, FishProvider
from ff14angler.dataClasses.spot.spotProvider import Spot, SpotProvider


T1 = TypeVar('T1')
T2 = TypeVar('T2')


class HomePage:

    # noinspection SpellCheckingInspection
    @staticmethod
    async def _dict_awaiter(key: T1, value: Awaitable[T2]) -> Tuple[T1, T2]:
        return key, await value

    @classmethod
    async def _parse_bait_list(cls, bait_parent: Tag) -> Dict[int, Bait]:
        temp_bait_list: List[Awaitable[Bait]] = []

        for tag in sorted(bait_parent.find_all('option'), key=lambda x: int(x.attrs['value'])):  # type: Tag
            angler_bait_id: int = int(tag.attrs['value'])
            angler_bait_name: str = tag.text.strip()

            if angler_bait_name not in {'Select Bait'}:
                temp_bait_list.append(BaitProvider.get_bait_from_angler_bait(angler_bait_id, angler_bait_name))

        await asyncio.gather(*temp_bait_list)
        return BaitProvider.bait_holder

    @classmethod
    async def _parse_fish_list(cls, fish_parent: Tag):
        temp_fish_list: List[Awaitable[Fish]] = []

        for tag in sorted(fish_parent.find_all('option'), key=lambda x: int(x.attrs['value'])):  # type: Tag
            angler_fish_id: int = int(tag.attrs['value'])
            angler_fish_name: str = tag.text.strip()

            if angler_fish_name != 'Select Fish':
                temp_fish_list.append(FishProvider.get_fish_from_angler_fish(angler_fish_id, angler_fish_name))

        await asyncio.gather(*temp_fish_list)
        return FishProvider.fish_holder

    @classmethod
    async def _parse_spot_list(cls, spot_parent: Tag):
        temp_spot_list: List[Awaitable[Spot]] = []

        # noinspection SpellCheckingInspection
        for zone in spot_parent.find_all('optgroup'):  # type: Tag
            for spot in zone.find_all('option'):  # type: Tag
                spot_angler_id: int = int(spot.attrs['value'])
                spot_angler_name: str = spot.text.strip()
                spot_angler_zone_name: str = zone.attrs['label']

                temp_spot_list.append(
                    SpotProvider.get_spot_from_angler_spot(
                        spot_angler_id,
                        spot_angler_name,
                        spot_angler_zone_name
                    )
                )

        await asyncio.gather(*temp_spot_list)
        return SpotProvider.spot_holder

    @classmethod
    async def parse_homepage_data(cls, html: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html, lxml.__name__)

        return {
            'bait': await cls._parse_bait_list(soup.find('select', {'name': 'bait'})),
            'fish': await cls._parse_fish_list(soup.find('select', {'name': 'fish'})),
            'spot': await cls._parse_spot_list(soup.find('select', {'name': 'spot'}))
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