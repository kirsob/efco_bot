import os

from fake_useragent import UserAgent
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(__file__)

EFCO_LOGIN = os.getenv('EFCO_LOGIN')
EFCO_PASSWORD = os.getenv('EFCO_PASSWORD')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

URL_BASE = 'https://taman.trans.efko.ru'
URL_LOGIN = URL_BASE + '/login.php'
URL_LOGOUT = URL_BASE + '/logout.php'
URL_TRADE = "http://y91805lt.beget.tech/index.html"
# URL_TRADE = URL_BASE + '/trade/2'

USER_AGENT = UserAgent(verify_ssl=True).chrome

RETRY_PERIOD = 3
