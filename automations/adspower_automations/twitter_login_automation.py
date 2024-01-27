from automations.adspower_automations import workers


def twitter_login_automation(machine_info):
    pass


def run(ads_host: str, ads_key: str, machines: list, human_like: bool = True, debug_mode: bool = False):
    print(f"DEBUG: Running Twitter Login Automation") if debug_mode else None
    workers.run(ads_host, ads_key, machines, twitter_login_automation, human_like, debug_mode)
    return


if __name__ == "__main__":
    run(
        "http://local.adspower.net:50325",
        "7f82846fd1f111f50e89ae0598620aaa",
        ["3001"],
    )