# Opened AdsPower (for batch automations)
import automations.adspower_automations.ads_browser_unit

opened_browsers = []

# This file saved all ID of AdsPower's machine
file_contents = ['3001']


def run(ads_host: str, ads_key: str, debug_mode: bool = False):
    print("DEBUG: Running Berachain Galxe Automation") if debug_mode else None
    for machine_id in file_contents:
        print(f"DEBUG: Creating a new Ads Browser instance for machine {machine_id}") if debug_mode else None
        browser = automations.adspower_automations.ads_browser_unit.AdsBrowserUnit(
            ads_host, ads_key, machine_id)
        # Save current opened browser for operation
        current_opened_browser = browser.start(debug_mode)
        opened_browsers.append(current_opened_browser)
        print(f"DEBUG: Created an AdsPower Browser with {browser.user_id}") if debug_mode else None

        # Just do the automation one by one.
        print(f"DEBUG: Doing the automation one by one") if debug_mode else None
        # With selenium package
        selenium_address = current_opened_browser['data']['ws']['selenium']
        print(selenium_address)
        # Set Chrome options to specify the debugging address
        chrome_options = Options()


class BerachainGalxeAutomation:
    def __init__(self):
        pass