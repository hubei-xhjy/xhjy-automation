import automations.twitter_login
from automations import ads_browser_unit
import pandas as pd
from threading import Thread, Semaphore

API_HOST = 'http://local.adspower.net:50325'
API_KEY = '7f82846fd1f111f50e89ae0598620aaa'

machine_working_together_limit = 2
semaphore = Semaphore(machine_working_together_limit)

def twitter_login(machine_info):
    with semaphore:
        ads_serial_no = machine_info['AdsSerialNo']
        email = machine_info['Email']
        twitter_username = machine_info['TwitterUsername']
        twitter_password = machine_info['TwitterPassword']
        twitter_2fa = machine_info['Twitter2FA']
        browser = ads_browser_unit.AdsBrowserUnit(API_HOST, API_KEY, ads_serial_no)
        automations.twitter_login.run(browser, email, twitter_username, twitter_password, twitter_2fa)


if __name__ == '__main__':
    threads = []
    df = pd.read_csv('./private/machine_info.csv')
    # TODO: for loop the machines
    for i in range(25, 31):
        t = Thread(target=twitter_login, args=(df.iloc[i - 1],))
        threads.append(t)
        t.start()
