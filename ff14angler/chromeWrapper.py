#! /usr/env/bin/ python3

import os

from selenium import webdriver


class ChromeWrapper:
    """Selenium chrome driver wrapper so I stop making one off selenium setups."""

    def __init__(self, download_directory=False, headless=False, manual=False, maximized=True):
        """Init for ChromeWrapper."""
        self.options = self.setup_config_options(download_directory, headless, maximized)
        self.get_chrome_install_location(manual)

        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.enable_download(download_directory)

    def __enter__(self):
        """Make driver available in a with context.."""
        return self.driver

    def __exit__(self, exception_type, exception_val, trace):
        """Properly close driver."""
        self.driver.quit()

    @staticmethod
    def setup_config_options(download_directory, headless, maximized):
        """Setup default chrome config options."""
        options = webdriver.ChromeOptions()

        # noinspection SpellCheckingInspection
        config = {
            'profile.default_content_settings.popups': 0,
            'download.prompt_for_download': 'false',
            'profile.default_content_setting_values.automatic_downloads': True,
            'safebrowsing.enabled': False
        }

        if download_directory:

            config['download.default_directory'] = download_directory

        if headless:

            options.add_argument('--headless')

        if maximized:

            options.add_argument('--start-maximized')

        options.add_argument('--disable-gpu')
        # noinspection SpellCheckingInspection
        options.add_experimental_option('prefs', config)

        return options

    def get_chrome_install_location(self, manual):
        """Get the install location for the chrome executable."""
        if manual:

            if os.path.isfile(manual):

                self.options.binary_location = manual

            else:

                raise FileNotFoundError(
                    'The manual chrome executable location was not found: {}'.format(manual)
                )

        default_binary_paths = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium']

        for binary in default_binary_paths:
            if os.path.isfile(binary):
                self.options.binary_location = binary
                return

        raise FileNotFoundError('Chrome install file not found.')

    def enable_download(self, download_directory):
        """Add missing support for chrome "send_command" to selenium web driver."""
        if download_directory:

            # noinspection PyProtectedMember
            self.driver.command_executor._commands['send_command'] = (
                'POST', '/session/$sessionId/chromium/send_command'
            )

            self.driver.execute(
                'send_command',
                {
                    'cmd': 'Page.setDownloadBehavior',
                    'params': {
                        'behavior': 'allow',
                        'downloadPath': download_directory
                    }
                }
            )
