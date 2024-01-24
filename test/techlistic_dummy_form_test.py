import unittest

from selenium.webdriver import Keys

from automations.adspower_automations.ads_browser_unit import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here


class DummyFormTest(unittest.TestCase):
    def test_open_browser(self):
        browser = AdsBrowserUnit(
            'http://local.adspower.net:50325',
            '7f82846fd1f111f50e89ae0598620aaa',
            '3001',
            True,
            True
        )
        browser.start()
        browser.open_website('https://www.techlistic.com/p/selenium-practice-form.html')
        # Click cookie button
        browser.wait(2000)
        browser.click_element(BY_CSS, '#ez-accept-necessary') if browser.get_element(BY_CSS, '#ez-cookie-dialog') else None
        # Focus first name input box
        browser.scroll_to_element(BY_NAME, 'firstname')
        browser.focus_element(BY_NAME, 'firstname')
        browser.input('Hello, world!', BY_NAME, 'firstname')
        browser.scroll(1000)


if __name__ == '__main__':
    unittest.main()
