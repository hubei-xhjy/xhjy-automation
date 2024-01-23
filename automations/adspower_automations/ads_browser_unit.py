import urllib.parse
import urllib.request
import urllib.error
import json

from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chromium import webdriver


class AdsBrowserUnit:
    ads_host = ''
    ads_key = ''
    user_id = ''

    def __init__(self, ads_host: str, ads_key: str, user_id: str) -> None:
        self.ads_host = ads_host
        self.ads_key = ads_key
        self.user_id = user_id
        pass

    def start(self, debug_mode: bool) -> object:
        # Start browser api path
        api_path = '/api/v1/browser/start'

        get_params = {
            'serial_number': self.user_id
        }

        url_with_params = f"{self.ads_host}{api_path}?{urllib.parse.urlencode(get_params)}"
        print(f"DEBUG: try to GET url: {url_with_params}") if debug_mode else None

        try:
            # 发送请求并读取响应
            with urllib.request.urlopen(url_with_params) as response:
                # 读取响应内容
                response_data = response.read()

                # 解析 JSON 数据
                print("DEBUG: Opened Ads Browser, response:") if debug_mode else None
                print(response_data) if debug_mode else None
                self.__open_browser__(json.loads(response_data), debug_mode=debug_mode)
                return json.loads(response_data)
        except urllib.error.URLError as e:
            # TODO: 处理连接错误
            print(f"URL Error: {e.reason}")
            return {}
        except Exception as e:
            # TODO: 处理其他错误
            print(f"An error occurred: {e}")
            return {}

    def __open_browser__(self, browser_data: {}, debug_mode: bool) -> bool:
        """
        open ads browser and save the driver in cache.
        :param debug_mode:
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

    def open_website(self, url: str, debug_mode: bool = False):
        print(f"DEBUG: Opening website {url}, please wait...") if debug_mode else None
        self.driver.get(url)