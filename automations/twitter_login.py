import random

import automations.ads_browser_unit as aconst
from automations.ads_browser_unit import AdsBrowserUnit


def run(browser: AdsBrowserUnit, email: str, username: str, password: str, two_fa: str):
    browser.open_website('https://x.com')
    # Check for cookie popup
    if browser.element_exists(aconst.BY_XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]/div/span/span'):
        cookie_buttons = [
            browser.find_element(aconst.BY_XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[1]'),
            browser.find_element(aconst.BY_XPATH, '//*[@id="layers"]/div/div/div/div/div/div[2]/div[2]')
        ]
        browser.click(elements=cookie_buttons)
    # Click sign-in button, and wait for login screen
    sign_in_button = browser.find_element(aconst.BY_CSS_SELECTOR, '[data-testid="loginButton"]')
    browser.click(element=sign_in_button, wait_for_millis=5000)
    # Input email or username
    text_to_input = username if random.randint(0, 1) else email
    user_input_box = browser.find_element(aconst.BY_CSS_SELECTOR, '[autocomplete="username"]')
    browser.input_text(text_to_input, user_input_box)
    # Input password
    password_box = browser.find_element(aconst.BY_CSS_SELECTOR, '[autocomplete="current-password"]')
    next_step_button = browser.find_element(aconst.BY_CSS_SELECTOR, '[data-testid="LoginForm_Login_Button"][role="button"]')
    browser.input_text(password, password_box, next_step_element=next_step_button)
    # Input TOTP
    totp_input_box = browser.find_element(aconst.BY_CSS_SELECTOR, '[data-testid="ocfEnterTextTextInput"][type="text"]')
    next_step_button = browser.find_element(aconst.BY_CSS_SELECTOR, '[data-testid="ocfEnterTextNextButton"][role="button"]')
    current_totp = browser.generate_totp(two_fa)
    browser.input_text(current_totp, totp_input_box, next_step_element=next_step_button)
    # Terms of Service pop-up
    browser.click_if_exists(aconst.BY_XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div')
    pass
