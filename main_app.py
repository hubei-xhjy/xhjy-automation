import automations.adspower_automations.berachain_galxe_automation as berachain_automation
from tools.account_list_converters import twitter_list_converter


DEBUG_MODE_ASCII = r"""
   ___      __               __  ___        __   
  / _ \___ / /  __ _____ _  /  |/  /__  ___/ /__ 
 / // / -_) _ \/ // / _ `/ / /|_/ / _ \/ _  / -_)
/____/\__/_.__/\_,_/\_, / /_/  /_/\___/\_,_/\__/ 
                   /___/                         """

HUMAN_LIKE_ASCII = r"""
   __ __                         __   _ __      
  / // /_ ____ _  ___ ____  ____/ /  (_) /_____ 
 / _  / // /  ' \/ _ `/ _ \/___/ /__/ /  '_/ -_)
/_//_/\_,_/_/_/_/\_,_/_//_/   /____/_/_/\_\\__/ """


def convert_twitter_list():
    twitter_list_converter.convert_and_output(r"private/100_Twitters.sep", r"private/100_Twitters.csv")


class APP:
    debug_mode = False
    human_like = True
    ads_host = ""
    ads_key = ""
    opened_browser_data = []

    def __init__(self, ads_host, ads_key):
        self.ads_host = ads_host
        self.ads_key = ads_key
        pass

    def main_menu(self):
        print("Welcome to XHJY-automation tool.")
        while True:
            print("")
            print("==============================================================")
            print(DEBUG_MODE_ASCII) if self.debug_mode else None
            print(HUMAN_LIKE_ASCII) if self.human_like else None
            print("========================= Automations ========================")
            print("A1. Test Berachain Automation                                 ")
            print("A2. [Scheduled] GitHub Automation (commits, fork, stars, etc.)")
            print("========================= Analytics ==========================")
            print("An1. [Scheduled] Analysis BTC pass-year's                     ")
            print("========================= Converters =========================")
            print("C1. Convert Twitter list purchased from Twitter888.cn         ")
            print("========================= Systems ============================")
            print("Debug. DEBUG MODE                                             ") if self.debug_mode else None
            print("Debug. Debug Mode                                             ") if not self.debug_mode else None
            print("Human. HUMAN LIKE (Will wait for a while before continuing)   ") if self.human_like else None
            print("Human. Human Like (Will wait for a while before continuing)   ") if not self.human_like else None
            print("Q    . Exit Application                                       ")
            print("==============================================================")
            choice = input("Please choose an option: ").lower()

            if choice == "a1":
                print("DEBUG: Running Berachain Automation") if self.debug_mode else None
                berachain_automation.run(self.ads_host, self.ads_key, self.human_like, self.debug_mode)
            elif choice == "c1":
                print("DEBUG: Running Twitter Account List Converter") if self.debug_mode else None
                convert_twitter_list()
            elif choice == "debug":
                self.debug_mode = not self.debug_mode
                print(f"_Debug Mode is switch {'on' if self.debug_mode else 'off'}")
            elif choice == "human":
                self.human_like = not self.human_like
                print(f"_Human Like is switch {'on' if self.human_like else 'off'}")
            elif choice == "q":
                break
            else:
                print("Invalid option, please try again.")
            input("Press ENTER to continue...")
