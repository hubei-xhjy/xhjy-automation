import urllib.parse
import urllib.request
import urllib.error

import json
import time
import random
import os

from selenium.common import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

PATTERN_TYPE_URL = 'URL'
PATTERN_TYPE_TITLE = 'TITLE'

COND_EQUAL = 'EQUAL'
COND_NOT_EQUAL = 'NOT_EQUAL'
COND_CONTAINS = 'CONTAINS'
COND_NOT_CONTAINS = 'NOT_CONTAINS'

BY_CSS = 'CSS'
BY_ID = 'ID'
BY_NAME = 'NAME'
BY_XPATH = 'XPATH'
BY_TEXT = 'TEXT'

SEL_TYPE_FIXED = 'SEL_TYPE_FIXED'
SEL_TYPE_RANDOM = 'SEL_TYPE_RANDOM'


class AdsBrowserUnit:
    user_id = ''

    def __init__(self, ads_host: str, ads_key: str, user_id: str, human_like: bool, debug_mode: bool) -> None:
        self.original_window = None
        self.ads_host = ads_host
        self.ads_key = ads_key
        self.user_id = user_id
        self.debug_mode = debug_mode
        self.human_like = human_like

    def start(self) -> object:
        # Start browser api path
        api_path = '/api/v1/browser/start'

        get_params = {
            'serial_number': self.user_id
        }

        url_with_params = f"{self.ads_host}{api_path}?{urllib.parse.urlencode(get_params)}"
        print(f"DEBUG: try to GET url: {url_with_params}") if self.debug_mode else None

        try:
            # 发送请求并读取响应
            with urllib.request.urlopen(url_with_params) as response:
                # 读取响应内容
                response_data = response.read()

                # 解析 JSON 数据
                print("DEBUG: Opened Ads Browser, response:") if self.debug_mode else None
                print(response_data) if self.debug_mode else None
                self.__connect_selenium__(json.loads(response_data))
                return json.loads(response_data)
        except urllib.error.URLError as e:
            # TODO: 处理连接错误
            print(f"URL Error: {e.reason}")
            return {}
        except Exception as e:
            # TODO: 处理其他错误
            print(f"An error occurred: {e}")
            return {}

    def __mimic_human_wait__(self):
        if self.human_like:
            # Wait in range 300 to 1000
            wait_time = random.randrange(300, 1000) / 1000
            print(f"DEBUG: [Human Like] Waiting {wait_time} seconds.") if self.debug_mode else None
            time.sleep(wait_time)

    def __mimic_human_long_wait__(self):
        if self.human_like:
            # Wait in range 300 to 1000
            wait_time = random.randrange(700, 2000) / 1000
            print(f"DEBUG: [Human Like] Waiting {wait_time} seconds.") if self.debug_mode else None
            time.sleep(wait_time)

    def __connect_selenium__(self, browser_data: {}):
        """
        open ads browser and save the driver in cache.
        :return:
        """
        # With selenium package
        selenium_address = browser_data['data']['ws']['selenium']
        # Set Chrome options to specify the debugging address
        chrome_options = ChromiumOptions()
        chrome_options.add_experimental_option('debuggerAddress', selenium_address)
        # Set the webdriver path
        webdriver_path = browser_data['data']['webdriver']
        service = ChromiumService(webdriver_path)
        # Create a Webdriver instance
        self.driver = webdriver.ChromiumDriver(service=service, options=chrome_options)

    def __element_selector__(self, by: str, value: str, sel_type: str, order: int, order_max: int) -> WebElement:
        order -= 1
        order_max -= 1
        try:
            elements = None
            if by == BY_CSS:
                elements = self.driver.find_elements(By.CSS_SELECTOR, value)
            elif by == BY_NAME:
                elements = self.driver.find_elements(By.NAME, value)
            elif by == BY_ID:
                elements = self.driver.find_elements(By.ID, value)
            elif by == BY_XPATH:
                elements = self.driver.find_elements(By.XPATH, value)
            elif by == BY_TEXT:
                elements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{value}')]")
            else:
                raise ValueError(f"Unknown selector type: {by}")

            if not elements:
                print(f"No elements found with {by} = '{value}'")
                return None

            if sel_type == SEL_TYPE_FIXED:
                return elements[min(order, len(elements) - 1)]
            elif sel_type == SEL_TYPE_RANDOM:
                max_index = min(order_max, len(elements)) - 1
                random_index = random.randint(0, max_index)
                return elements[random_index]
            else:
                raise ValueError(f"Unknown selection type: {sel_type}")

        except NoSuchElementException:
            print(f"No element found with {by} = '{value}'")
            return None

    def wait(self, min_millis: int, max_millis: int = 0):
        if max_millis > min_millis:
            wait_sec = random.randint(min_millis, max_millis) / 1000.0
        else:
            wait_sec = min_millis / 1000.0
        print(f"DEBUG: Waiting for {wait_sec}") if self.debug_mode else None
        time.sleep(wait_sec)

    def open_website(self, url: str):
        print(f"DEBUG: Opening website {url}, please wait...") if self.debug_mode else None
        self.driver.get(url)
        self.__mimic_human_wait__()

    def new_tab(self):
        print(f"DEBUG: Create a new tab") if self.debug_mode else None
        self.driver.switch_to.new_window('tab')
        self.__mimic_human_wait__()

    def close_tab(self, and_focus_tab: str = ''):
        print(f"DEBUG: Close tab") if self.debug_mode else None
        self.driver.close()
        self.driver.switch_to.window(self.original_window)
        self.__mimic_human_wait__()

    def close_other_tabs(self):
        print(f"DEBUG: Close other tabs") if self.debug_mode else None
        original_tab = self.driver.current_window_handle
        for tab in self.driver.window_handles:
            if tab != original_tab:
                self.driver.switch_to.window(tab)
                self.driver.close()
        self.__mimic_human_wait__()

    def switch_to_tab(self, tab_info_pattern: str, pattern_type: str, conditions: str):
        print(f"DEBUG: Switch to tab {tab_info_pattern}, with conditions {conditions} in {pattern_type}") if self.debug_mode else None
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            try:
                current_info = self.driver.current_url if pattern_type == PATTERN_TYPE_URL else self.driver.title
                if (
                        (conditions == COND_EQUAL and current_info == tab_info_pattern) or
                        (conditions == COND_NOT_EQUAL and current_info != tab_info_pattern) or
                        (conditions == COND_CONTAINS and tab_info_pattern in current_info) or
                        (conditions == COND_NOT_CONTAINS and tab_info_pattern not in current_info)
                ):
                    self.__mimic_human_wait__()
                    return
            except NoSuchElementException:
                # 忽略不存在或已关闭的标签页
                continue
        print("No tab matching the specified criteria was found.")

    def page_refresh(self):
        print(f"DEBUG: Page refresh") if self.debug_mode else None
        self.driver.refresh()
        self.__mimic_human_wait__()

    def page_backward(self):
        print(f"DEBUG: Page backward") if self.debug_mode else None
        self.driver.back()
        self.__mimic_human_wait__()

    def page_forward(self):
        print(f"DEBUG: Page forward") if self.debug_mode else None
        self.driver.forward()
        self.__mimic_human_wait__()

    def take_screenshot(self, filename: str = user_id + str(time.time())):
        if not os.path.exists('screenshots'):
            print("DEBUG: Screenshots directory not found. Creating screenshots...") if self.debug_mode else None
            os.mkdir('screenshots')
        print("DEBUG: Capturing screenshot") if self.debug_mode else None
        self.driver.save_screenshot(f'screenshots/{filename}.png')
        self.__mimic_human_wait__()

    def take_screenshots_by_element(self, search_by: str, search_value,
                                    sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1,
                                    filename: str = user_id + str(time.time())):
        if not os.path.exists('screenshots'):
            print("DEBUG: Screenshots directory not found. Creating screenshots...") if self.debug_mode else None
            os.mkdir('screenshots')
        ele = self.__element_selector__(search_by, search_value, sel_type, order, order_max)
        print("DEBUG: Capturing screenshots") if self.debug_mode else None
        ele.screenshot(f'screenshots/{filename}.png')
        self.__mimic_human_wait__()

    def hover_element(self, search_by: str, search_value, sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1):
        print(f"DEBUG: Hovering element {search_value} by {search_by}") if self.debug_mode else None
        ele = self.__element_selector__(search_by, search_value, sel_type, order, order_max)
        ActionChains(self.driver).move_to_element(ele).perform()
        self.__mimic_human_wait__()
        return ele

    def select_drop_down_value(self,
                               search_by: str, search_value, sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1,
                               value_sel_type: str = SEL_TYPE_FIXED, value_sel_order: int = 1, value_sel_order_max: int = 1):
        # TODO: Haven't implement for now...
        # For develop documentation, please visit: https://www.browserstack.com/guide/select-class-in-selenium
        pass

    def focus_element(self, search_by: str, search_value, sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1):
        print(f"DEBUG: Focusing element {search_value} by {search_by}") if self.debug_mode else None
        ele = self.hover_element(search_by, search_value, sel_type, order, order_max)
        ele.click()
        self.__mimic_human_wait__()

    def click_element(self, search_by: str, search_value, sel_type: str = SEL_TYPE_FIXED, order: int = 1 , order_max = 1):
        print(f"DEBUG: Clicking element {search_value} by {search_by}") if self.debug_mode else None
        ele = self.hover_element(search_by, search_value, sel_type, order, order_max)
        ele.click()
        self.__mimic_human_wait__()

    def get_element(self, search_by: str, search_value, sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1):
        """
        Get an element exists in the browser
        :param search_by:
        :param search_value:
        :param sel_type:
        :param order:
        :param order_max:
        :return:
        """
        print(f"DEBUG: Getting element {search_by} by {search_value}") if self.debug_mode else None
        self.__mimic_human_wait__()
        return self.__element_selector__(search_by, search_value, sel_type, order, order_max)

    def input(self, string_to_input: str, search_by: str, search_value,
              sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1,
              input_interval = 150):
        print(f"DEBUG: Input {string_to_input} to {search_value} by {search_by}") if self.debug_mode else None
        target_element = self.get_element(search_by, search_value, sel_type, order, order_max)
        if self.human_like:
            # Input character one by one randomly waiting time
            for char in string_to_input:
                waiting_time = random.randint(150, 250) / 1000
                time.sleep(waiting_time)
                target_element.send_keys(char)
            pass
        else:
            # Input character in a specified speed
            waiting_time = input_interval / 1000
            for char in string_to_input:
                time.sleep(waiting_time)
                target_element.send_keys(char)
            pass
        self.__mimic_human_wait__()

    def scroll_to_element(self, search_by: str, search_value, sel_type: str = SEL_TYPE_FIXED, order: int = 1, order_max = 1):
        ele = self.get_element(search_by, search_value, sel_type, order, order_max)
        ActionChains(self.driver).move_to_element(ele)

    def __scroll_down__(self, distance: int, distance_between: int):
        total_scrolled = 0
        next_scroll_distance = total_scrolled
        min_dist_between_scrolls = 300
        max_dist_between_scrolls = 500
        while total_scrolled < distance:
            next_scroll_distance += random.randint(min_dist_between_scrolls, max_dist_between_scrolls)
            scroll_distance = next_scroll_distance - total_scrolled
            for i in range(scroll_distance):
                self.driver.execute_script(f'window.scrollBy(0, {i})')
                total_scrolled += i
                if total_scrolled >= distance / 2:
                    last_no = i
                    break
            for i in range(last_no, 0, -1):
                self.driver.execute_script(f"window.scrollBy(0, {i})")
            self.__mimic_human_long_wait__()

    def scroll(self, distance: int, distance_max: int = 0):
        min_dist_between_scrolls = 100
        max_dist_between_scrolls = 200
        min_delay_between_scrolls = 0.1
        max_delay_between_scrolls = 0.5

        total_distance = random.randint(distance, distance_max) if distance_max > distance else distance

        scrolled = 0
        while scrolled < total_distance:
            # 确保滚动距离范围有效
            max_scroll_dist = min(max_dist_between_scrolls, total_distance - scrolled)
            if max_scroll_dist < min_dist_between_scrolls:
                break

            scroll_distance = random.randint(min_dist_between_scrolls, max_scroll_dist)
            delay = random.uniform(min_delay_between_scrolls, max_delay_between_scrolls)

            self.driver.execute_script(f"window.scrollBy(0, {scroll_distance})")

            scrolled += scroll_distance
            time.sleep(delay)
