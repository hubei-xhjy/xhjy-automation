import main_app

API_HOST = 'http://local.adspower.net:50325'
API_KEY = '7f82846fd1f111f50e89ae0598620aaa'

# Show main menu

app = main_app.APP(API_HOST, API_KEY)
app.main_menu()

# Open AdsPower Browser by api
