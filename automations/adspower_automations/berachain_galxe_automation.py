# Opened AdsPower (for batch automations)
from automations.adspower_automations import ads_browser_unit
import automations.adspower_automations.ads_browser_unit

opened_browsers = []

# This file saved all ID of AdsPower's machine
file_contents = ['3001']


def run(ads_host: str, ads_key: str, human_like: bool, debug_mode: bool = False):
    """
    Run the automation
    :param ads_host:
    :param ads_key:
    :param debug_mode:
    :param human_like: if true, it will wait for a while then do the next step
    :return:
    """
    print("DEBUG: Running Berachain Galxe Automation") if debug_mode else None
    for machine_id in file_contents:
        print(f"DEBUG: Creating a new Ads Browser instance for machine {machine_id}") if debug_mode else None
        # Create an Ads browser
        browser = automations.adspower_automations.ads_browser_unit.AdsBrowserUnit(
            ads_host, ads_key, machine_id, human_like, debug_mode)
        # Save current opened browser for operation
        opened_browsers.append(browser)
        print(f"DEBUG: Created an AdsPower Browser with {browser.user_id}") if debug_mode else None

        # Control the browser
        browser.start()
        browser.open_website('https://galxe.com/Berachain/campaign/GCjGGttCAG')
        browser.hover_element(ads_browser_unit.BY_XPATH, '//*[@id="ga-campaign-collection-page"]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div/div[1]/a/div/div[3]')