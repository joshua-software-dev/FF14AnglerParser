#! /usr/bin/env python3

import base64
import os

from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support import expected_conditions  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore

from ff14angler.constants.javascript import fetch_large_url_data_from_lodestone_page
from ff14angler.constants.values import ANGLER_PAGE_LOAD_WAIT_DURATION, config_settings


class LodestoneImageScraper:

    @classmethod
    async def fetch_large_image_from_lodestone_url(cls, driver: WebDriver, url: str) -> bytes:
        print(f'Scraping lodestone url: {url}')
        driver.get(url)

        WebDriverWait(driver, ANGLER_PAGE_LOAD_WAIT_DURATION).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, '.db-view__item__icon__item_image.sys_nq_element')
            )
        )

        img_data_url: str = driver.execute_async_script(fetch_large_url_data_from_lodestone_page)
        return base64.b64decode(img_data_url.split(',')[1])

    @classmethod
    async def get_large_icon(
        cls,
        driver: WebDriver,
        short_icon_url: str,
        lodestone_url: str
    ) -> str:
        # (BASE_URL)/i/006000/010110.png -> (BASE_URL)/i/006000/010110l.png
        large_icon_url: str = short_icon_url.replace('.png', 'l.png')

        # i/006000/010110l.png -> (EXPORT_DIR)/i/006000/010110l.png
        large_icon_path: str = os.path.join(
            config_settings['EXPORT_DIRECTORY'],
            # /i/006000/010110l.png -> i/006000/010110l.png
            large_icon_url.lstrip('/')
        )

        os.makedirs(os.path.dirname(large_icon_path), exist_ok=True)
        if not os.path.isfile(large_icon_path):
            img_bytes = await cls.fetch_large_image_from_lodestone_url(driver, lodestone_url)
            with open(large_icon_path, 'wb+') as fh:
                fh.write(img_bytes)

        return large_icon_url
