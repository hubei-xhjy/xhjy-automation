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
        opened_browsers.append(browser.start(debug_mode))
        print(f"DEBUG: Created an AdsPower Browser with {browser.user_id}") if debug_mode else None


class BerachainGalxeAutomation:
    def __init__(self):
        pass