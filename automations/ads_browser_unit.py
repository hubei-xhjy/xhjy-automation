from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError

import json

from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BY_ID = By.ID
BY_NAME = By.NAME
BY_TAG_NAME = By.TAG_NAME
BY_CLASS_NAME = By.CLASS_NAME
BY_CSS_SELECTOR = By.CSS_SELECTOR
BY_XPATH = By.XPATH

KEY_RETURN = Keys.RETURN


class AdsBrowserUnit:
    driver: ChromiumDriver

    def __init__(self, ads_host: str, ads_key: str, serial_no: str,
                 human_like: bool = True, debug_mode: bool = False):
        self.ads_host = ads_host
        self.ads_key = ads_key
        self.serial_no = serial_no
        self.human_like = human_like
        self.debug_mode = debug_mode
        self.__start__()
        return

    def __start__(self):
        """
        Start the ads browser, and connect to the selenium
        :return:
        """
        print(f"DEBUG: Starting ads browser for {self.serial_no}") if self.debug_mode else None
        api_path = '/api/v1/browser/start'
        get_params = {
            'serial_number': self.serial_no
        }
        url = f'{self.ads_host}{api_path}?{urlencode(get_params)}'
        print(f"DEBUG: Try to GET url: {url}") if self.debug_mode else None

        try:
            # Send request and read the response data
            with urlopen(url) as response:
                response_data = response.read().decode('utf-8')
                print(f"DEBUG: Ads browser opened with response: {response_data}") if self.debug_mode else None
                # Resolve JSON data
                response_json = json.loads(response_data)
                # Connect Selenium
                print(f"DEBUG: Connecting with Selenium driver") if self.debug_mode else None
                selenium_address = response_json['data']['ws']['selenium']
                webdriver_path = response_json['data']['webdriver']
                print(f"DEBUG: Set Chromium options to specify the debugging address: {selenium_address}") if self.debug_mode else None
                chromium_options = ChromiumOptions()
                chromium_options.add_experimental_option('debuggerAddress', selenium_address)
                print(f"DEBUG: Set the webdriver path to chromedriver") if self.debug_mode else None
                service = ChromiumService(webdriver_path)
                print(f"DEBUG: Create a webdriver instance") if self.debug_mode else None
                self.driver = ChromiumDriver(service=service, options=chromium_options)
        except URLError as e:
            print(f"ERROR: URLError {e.reason}")
            return
        except Exception as e:
            print(f"ERROR: Unexpected error {e}")
            return
        return

    def stop(self):
        """
        Close the instance
        :return:
        """
        self.driver.quit()
        return

    def wait(self, timeout: float = 500):
        return

    def short_wait(self, timeout: float = 300, timeout_max: float = 1000):
        return

    def long_wait(self, timeout: float = 1000, timeout_max: float = 5000):
        return

    def open_website(self, url: str):
        """
        Open a webpage
        :param url:
        :return:
        """
        return

    def new_tab(self, with_url: str = ''):
        """
        Create a new tab in the browser, and redirect to the url if set
        :param with_url:
        :return:
        """
        return

    def close_tab(self):
        return

    def close_other_tabs(self):
        return

    def switch_to_tab(self, pattern: str = '', pattern_value: str = '', tab_index: int = -1):
        return

    def page_refresh(self):
        return

    def page_backward(self):
        return

    def page_forward(self):
        return

    def take_screenshot(self):
        self.driver.fin
        return
