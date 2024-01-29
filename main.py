import time

import selenium.webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chromium.webdriver import ChromiumDriver
from selenium.webdriver.remote.webelement import WebElement

from automations import ads_browser_unit
import pandas as pd
from threading import Thread, Semaphore
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random

import pyotp

API_HOST = 'http://local.adspower.net:50325'
API_KEY = '7f82846fd1f111f50e89ae0598620aaa'

machine_working_together_limit = 2


def input_character_one_by_one(driver: ChromiumDriver, string: str, element: WebElement, next_step_element: WebElement = None):
    element.click()
    time.sleep(random.randrange(1500, 2500) / 1000)
    for char in string:
        waiting_time = random.randint(150, 250) / 1000
        time.sleep(waiting_time)
        element.send_keys(char)
    time.sleep(random.randrange(500, 1500) / 1000)
    if next_step_element is not None and random.randint(0, 1) == 0:
        ActionChains(driver).move_to_element(next_step_element).perform()
        time.sleep(random.randint(500, 1000) / 1000)
        next_step_element.click()
    else:
        element.send_keys(Keys.RETURN)


def twitter_automation(machine_info):
    with semaphore:
        print('Starting Twitter automation')
        ads_serial_no = machine_info['AdsSerialNo']
        email = machine_info['Email']
        twitter_username = machine_info['TwitterUsername']
        twitter_password = machine_info['TwitterPassword']
        twitter_2fa = machine_info['Twitter2FA']
        browser = ads_browser_unit.AdsBrowserUnit(API_HOST, API_KEY, ads_serial_no, debug_mode=True)

        # Open Twitter website
        browser.driver.get('https://x.com')
        time.sleep(random.randint(4000, 5000) / 1000)

        # Check for cookie button
        cookie_popup = browser.driver.find_elements(By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div/span/span')
        if cookie_popup:
            cookie_buttons_xpath = [
                '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]',
                '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]'
            ]
            cookie_button = browser.driver.find_element(By.XPATH, random.choice(cookie_buttons_xpath))
            wait_time = random.randrange(2000, 5000) / 1000
            ActionChains(browser.driver).move_to_element(cookie_button).pause(wait_time).click().perform()

        # Click sign-in button
        sign_in_button = browser.driver.find_element(By.CSS_SELECTOR, '[data-testid="loginButton"]')
        wait_time = random.randrange(2000, 5000) / 1000
        ActionChains(browser.driver).move_to_element(sign_in_button).pause(wait_time).click().perform()

        # Wait for login screen popup
        time.sleep(random.randrange(4000, 5000) / 1000)

        # Input Email(0) or Username(1)
        user = email if random.randint(0, 1) == 0 else twitter_username
        user_input_box = browser.driver.find_element(By.CSS_SELECTOR, '[autocomplete="username"]')
        input_character_one_by_one(browser.driver, user, user_input_box)
        time.sleep(random.randrange(4000, 5000) / 1000)

        # Input Password
        password_input_box = browser.driver.find_element(By.CSS_SELECTOR, '[autocomplete="current-password"]')
        next_step_button = browser.driver.find_element(By.CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"][role="button"]')
        input_character_one_by_one(browser.driver, twitter_password, password_input_box, next_step_button)
        time.sleep(random.randrange(4000, 5000) / 1000)

        # Input TOTP
        totp_input_box = browser.driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"][type="text"]')
        next_step_button = browser.driver.find_element(By.CSS_SELECTOR, '[data-testid="ocfEnterTextNextButton"][role="button"]')
        totp = pyotp.TOTP(twitter_2fa)
        current_totp = totp.now()
        input_character_one_by_one(browser.driver, current_totp, totp_input_box, next_step_button)
        time.sleep(random.randrange(4000, 5000) / 1000)

        # Terms of Service pop-up
        tos_popup = browser.driver.find_elements(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div')
        if tos_popup:
            tos_popup_button = browser.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div')
            wait_time = random.randrange(2000, 5000) / 1000
            ActionChains(browser.driver).move_to_element(tos_popup_button).pause(wait_time).click().perform()

        time.sleep(3)
        browser.driver.quit()
    pass


semaphore = Semaphore(machine_working_together_limit)
if __name__ == '__main__':
    threads = []
    df = pd.read_csv('./private/machine_info.csv')
    # TODO: for loop the machines
    for i in [15, 16, 17, 19]:
        t = Thread(target=twitter_automation, args=(df.iloc[i - 1],))
        threads.append(t)
        t.start()
