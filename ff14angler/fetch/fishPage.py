#! /usr/bin/env python3

import asyncio
import urllib.parse

import lxml  # type: ignore

from bs4 import BeautifulSoup  # type: ignore
from selenium.common.exceptions import TimeoutException  # type: ignore
from selenium.webdriver.chrome.webdriver import WebDriver  # type: ignore
from selenium.webdriver.common.by import By  # type: ignore
from selenium.webdriver.support.ui import WebDriverWait  # type: ignore
from selenium.webdriver.support import expected_conditions  # type: ignore

from ff14angler.constants.values import (
    ANGLER_BASE_URL,
    ANGLER_PAGE_LOAD_WAIT_DURATION,
    ANGLER_DELAY_BETWEEN_REQUESTS_DURATION
)
from ff14angler.dataClasses.comment.commentSection import CommentSection
from ff14angler.dataClasses.fish.fish import Fish
from ff14angler.dataClasses.fish.fishProvider import FishProvider
from ff14angler.fetch.lodestoneImageScraper import LodestoneImageScraper
from ff14angler.network.delayOnReleaseLock import DelayOnReleaseLock


class FishPage:

    @staticmethod
    async def update_fish_with_large_icon_url(driver: WebDriver, fish: Fish):
        if fish.fish_angler_lodestone_url:
            if fish.fish_icon_url is None:
                raise ValueError(f'Missing icon url from xivapi: {fish}')

            fish.fish_large_icon_url = await LodestoneImageScraper.get_large_icon_and_url(
                driver=driver,
                short_icon_url=fish.fish_icon_url,
                lodestone_url=fish.fish_angler_lodestone_url
            )

    @staticmethod
    async def update_fish_desynthesis_items_with_large_icon_url(driver: WebDriver, fish: Fish):
        for desynthesis_item in fish.fish_angler_desynthesis_items:
            if desynthesis_item.desynthesis_angler_lodestone_url:
                if desynthesis_item.desynthesis_icon_url is None:
                    raise ValueError(f'Missing icon url from xivapi: {desynthesis_item}')

                desynthesis_item.desynthesis_large_icon_url = await LodestoneImageScraper.get_large_icon_and_url(
                    driver=driver,
                    short_icon_url=desynthesis_item.desynthesis_icon_url,
                    lodestone_url=desynthesis_item.desynthesis_angler_lodestone_url
                )

    @staticmethod
    async def update_fish_involved_recipes_with_large_icon_url(driver: WebDriver, fish: Fish):
        for recipe in fish.fish_angler_involved_recipes:
            if recipe.recipe_angler_lodestone_url:
                if recipe.recipe_icon_url is None:
                    raise ValueError(f'Missing icon url from xivapi: {recipe}')

                recipe.recipe_large_icon_url = await LodestoneImageScraper.get_large_icon_and_url(
                    driver=driver,
                    short_icon_url=recipe.recipe_icon_url,
                    lodestone_url=recipe.recipe_angler_lodestone_url
                )

    @classmethod
    async def collect_fish_data(cls, driver: WebDriver):
        fish_url_template = urllib.parse.urljoin(ANGLER_BASE_URL, '/fish/')
        lock = DelayOnReleaseLock(ANGLER_DELAY_BETWEEN_REQUESTS_DURATION)

        for fish_id, fish in FishProvider.fish_holder.items():
            angler_url: str = urllib.parse.urljoin(fish_url_template, str(fish_id))
            for attempt in range(3):
                driver.get('about:blank')
                print(f'Scraping page: {angler_url}')
                driver.get(angler_url)

                try:
                    WebDriverWait(driver, ANGLER_PAGE_LOAD_WAIT_DURATION).until(
                        expected_conditions.presence_of_element_located(
                            (By.CSS_SELECTOR, 'form.comment_form')
                        )
                    )

                    async with lock:
                        await asyncio.sleep(2)
                        html: str = driver.page_source

                        await fish.update_fish_with_comment_section(
                            await CommentSection.get_comment_section_from_web_driver(driver)
                        )
                    break
                except (TimeoutException, ValueError):
                    if attempt == 2:
                        raise

            await fish.update_fish_with_fish_soup(BeautifulSoup(html, lxml.__name__))
            await cls.update_fish_with_large_icon_url(driver, fish)
            await cls.update_fish_desynthesis_items_with_large_icon_url(driver, fish)
            await cls.update_fish_involved_recipes_with_large_icon_url(driver, fish)
