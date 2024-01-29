import threading
import time
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError

import json
import random

import pyotp
from selenium.webdriver import ActionChains
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

BY_ID = By.ID
BY_NAME = By.NAME
BY_TAG_NAME = By.TAG_NAME
BY_CLASS_NAME = By.CLASS_NAME
BY_CSS_SELECTOR = By.CSS_SELECTOR
BY_XPATH = By.XPATH


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

    def wait(self, timeout: int = 1000, timeout_max: int = 2000) -> None:
        if timeout_max > timeout:
            wait_time = random.randrange(timeout, timeout_max) / 1000
        else:
            wait_time = timeout / 1000
        time.sleep(wait_time)

    def stop(self):
        """
        Close the instance
        :return:
        """
        self.driver.quit()

        api_path = '/api/v1/browser/stop'
        get_params = {
            'serial_number': self.serial_no
        }
        url = f'{self.ads_host}{api_path}?{urlencode(get_params)}'
        print(f"DEBUG: Try to GET url: {url}") if self.debug_mode else None
        try:
            # Send request and read the response data
            with urlopen(url) as response:
                response_data = response.read().decode('utf-8')
                print(f"DEBUG: Ads browser close with response: {response_data}") if self.debug_mode else None
        except URLError as e:
            print(f"ERROR: URLError {e.reason}")
            return
        except Exception as e:
            print(f"ERROR: Unexpected error {e}")
            return
        return

    def open_website(self, url: str):
        self.driver.get(url)
        self.wait(4000, 5000)
        return

    def find_element(self, by: str, value: str):
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element(by, value))
        return self.driver.find_element(by, value)

    def find_elements(self, by: str, value: str) -> list[WebElement]:
        return self.driver.find_elements(by, value)

    def element_exists(self, by: str, value: str) -> bool:
        self.wait()
        return len(self.driver.find_elements(by, value)) > 0

    def click(self, element: WebElement = None, elements: list[WebElement] = None, wait_for_millis: int = 1000):
        if elements is not None:
            ele = random.choice(elements)
        else:
            ele = element
        wait_time = random.randrange(2000, 5000) / 1000
        ActionChains(self.driver).move_to_element(ele).pause(wait_time).click().perform()
        self.wait(wait_for_millis)

    def click_if_exists(self, by: str, value: str):
        if self.element_exists(by, value):
            ele = self.find_element(by, value)
            self.click(ele)

    def input_text(self, text: str, element: WebElement,
                   auto_next_step: bool = True, next_step_element: WebElement = None):
        self.click(element)
        for char in text:
            self.wait(150, 250)
            element.send_keys(char)
        if auto_next_step:
            if next_step_element is not None and random.randint(0, 1):
                wait_time = random.randrange(1000, 1500) / 1000
                ActionChains(self.driver).move_to_element(next_step_element).pause(wait_time).click().perform()
            else:
                self.wait(timeout_max=1500)
                element.send_keys(Keys.RETURN)
        self.wait()

    def generate_totp(self, secret: str):
        totp = pyotp.TOTP(secret)
        return totp.now()

    # TODO: Haven't implemented yet
    def new_tab(self, with_url: str = ''):
        """
        Create a new tab in the browser, and redirect to the url if set
        :param with_url:
        :return:
        """
        return

    # TODO: Haven't implemented yet
    def close_tab(self):
        return

    # TODO: Haven't implemented yet
    def close_other_tabs(self):
        return

    # TODO: Haven't implemented yet
    def switch_to_tab(self, pattern: str = '', pattern_value: str = '', tab_index: int = -1):
        return

    # TODO: Haven't implemented yet
    def page_refresh(self):
        return

    # TODO: Haven't implemented yet
    def page_backward(self):
        return

    # TODO: Haven't implemented yet
    def page_forward(self):
        return

    # TODO: Haven't implemented yet
    def take_screenshot(self):
        return
