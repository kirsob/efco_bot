import os

from dotenv import load_dotenv

load_dotenv()

EFCO_LOGIN = os.getenv('EFCO_LOGIN')
EFCO_PASSWORD = os.getenv('EFCO_PASSWORD')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

URL_BASE = 'https://taman.trans.efko.ru'
URL_LOGIN = URL_BASE + '/login.php'
URL_LOGOUT = URL_BASE + '/logout.php'
URL_TRADE = "http://y91805lt.beget.tech/index.html"
# URL_TRADE = URL_BASE + '/trade/2'

RETRY_PERIOD = 3
