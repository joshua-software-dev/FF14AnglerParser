#! /usr/bin/env python3

import json

import lxml

from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class HomePage:

    @staticmethod
    async def parse_homepage_data(html: str) -> Dict[str, Dict[int, str]]:
        soup = BeautifulSoup(html, lxml.__name__)
        bait_parent: Tag = soup.find('select', {'name': 'bait'})
        fish_parent: Tag = soup.find('select', {'name': 'fish'})
        spot_parent: Tag = soup.find('select', {'name': 'spot'})

        bait_list: Dict[int, str] = {
            int(tag.attrs['value']): tag.text.strip() for tag in sorted(
                bait_parent.find_all('option'),
                key=lambda x: int(x.attrs['value'])
            )
        }

        fish_list: Dict[int, str] = {
            int(tag.attrs['value']): tag.text.strip() for tag in sorted(
                fish_parent.find_all('option'),
                key=lambda x: int(x.attrs['value'])
            )
        }

        spot_list: Dict[int, str] = {
            int(tag.attrs['value']): tag.text.strip() for tag in sorted(
                spot_parent.find_all('option'),
                key=lambda x: int(x.attrs['value'])
            )
        }

        del bait_list[0]  # 0 = 'Select Bait'
        del bait_list[2001]  # 2001 = 'Small' spearfishing head
        del bait_list[2002]  # 2002 = 'Normal' spearfishing head
        del bait_list[2003]  # 2003 = 'Large' spearfishing head

        del fish_list[0]  # 0 = 'Select Fish'

        del spot_list[0]  # 0 = 'Select Location'

        return {
            'bait': bait_list,
            'fish': fish_list,
            'spot': spot_list
        }

    @classmethod
    async def collect_homepage_data(cls, driver: WebDriver) -> Dict[str, Dict[int, str]]:
        driver.get('https://en.ff14angler.com/')

        try:
            WebDriverWait(driver, 10).until(
                expected_conditions.presence_of_element_located(
                    (By.ID, 'form_search')
                )
            )
        except TimeoutException:
            raise

        return await cls.parse_homepage_data(driver.page_source)
