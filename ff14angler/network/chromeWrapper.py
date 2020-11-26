#! /usr/env/bin/ python3

import os

from typing import Optional

from selenium import webdriver  # type: ignore
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class ChromeWrapper:
    """Selenium chromedriver wrapper so I stop making one off selenium setups."""

    def __init__(
        self,
        download_directory: Optional[str] = None,
        headless: bool = True,
        manual_binary_path: Optional[str] = None,
        start_maximized: bool = True
    ):
        """Init for ChromeWrapper."""
        self.driver: Optional[WebDriver] = None
        self.download_directory: Optional[str] = download_directory
        self.options = self.setup_config_options(
            download_directory,
            headless,
            manual_binary_path,
            start_maximized
        )

    def __enter__(self):
        """Make driver available in a with context.."""
        self.driver = webdriver.Chrome(chrome_options=self.options)

        if self.download_directory is not None:
            self.enable_download(self.driver, self.download_directory)

        return self.driver

    def __exit__(self, exception_type, exception_val, trace):
        """Properly close driver."""
        self.driver.quit()

    @classmethod
    def setup_config_options(
        cls,
        download_directory: Optional[str],
        headless: bool,
        manual_binary_path: Optional[str],
        start_maximized: bool
    ) -> Options:
        """Setup default chrome config options."""
        options = webdriver.ChromeOptions()
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-web-security')

        if headless:
            options.add_argument('--headless')

        if start_maximized:
            options.add_argument('--start-maximized')

        # noinspection SpellCheckingInspection
        options.add_argument(
            '--user-agent={}'.format(
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
            )
        )

        # noinspection SpellCheckingInspection
        config = {
            'download.prompt_for_download': False,
            'profile.default_content_settings.popups': 0,
            'profile.default_content_setting_values.automatic_downloads': True,
            'safebrowsing.enabled': False
        }

        if download_directory:
            config['download.default_directory'] = download_directory

        # noinspection SpellCheckingInspection
        options.add_experimental_option('prefs', config)
        return cls.get_binary_location(options, manual_binary_path)

    @staticmethod
    def get_binary_location(options: Options, manual_binary_path: Optional[str]) -> Options:
        """Get the install location for the cef executable."""
        if manual_binary_path is not None:

            if os.path.isfile(manual_binary_path):
                options.binary_location = manual_binary_path
            else:
                raise FileNotFoundError(
                    'The manual chrome/chromium executable location was not found: {}'.format(manual_binary_path)
                )

        default_binary_paths = [
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
            '/usr/bin/chromium',
            '/usr/lib64/chromium-browser/headless_shell'
        ]

        for binary in default_binary_paths:
            if os.path.isfile(binary):
                options.binary_location = binary
                return options

        raise FileNotFoundError('Chrome/Chromium binary file not found.')

    @staticmethod
    def enable_download(driver: WebDriver, download_directory: Optional[str]):
        """Add missing support for chrome "send_command" to selenium web driver."""
        if download_directory:
            # noinspection PyProtectedMember
            driver.command_executor._commands['send_command'] = (
                'POST', '/session/$sessionId/chromium/send_command'
            )

            driver.execute(
                'send_command',
                {
                    'cmd': 'Page.setDownloadBehavior',
                    'params': {
                        'behavior': 'allow',
                        'downloadPath': download_directory
                    }
                }
            )
