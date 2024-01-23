import urllib.parse
import urllib.request
import urllib.error
import json

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
                print(response_data)
                return json.loads(response_data)
        except urllib.error.URLError as e:
            # TODO: 处理连接错误
            print(f"URL Error: {e.reason}")
            return {}
        except Exception as e:
            # TODO: 处理其他错误
            print(f"An error occurred: {e}")
            return {}

