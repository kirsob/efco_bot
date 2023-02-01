from http import HTTPStatus
from sys import stdout

import requests
import logging
from config.config import (URL_TRADE, URL_LOGIN, URL_LOGOUT, URL_BASE,
                           EFCO_PASSWORD, EFCO_LOGIN, RETRY_PERIOD)
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime, time
import time
import os

script_dir = os.path.dirname(__file__)


UA = UserAgent(verify_ssl=True).chrome

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(stream=stdout)],
)


def login(session):
    try:
        response = session.post(
            URL_LOGIN,
            params={'xLogin': EFCO_LOGIN,
                    'xPassword': EFCO_PASSWORD},
            headers={'User-Agent': UA}
        )
    except requests.RequestException:
        logging.error('Запрос не удался')
        raise Exception('Запрос не удался')
    response.raise_for_status()


def logout(session):
    session.get(
        URL_LOGOUT,
        headers={'User-Agent': UA}
    )


def get_trade_page(session):
    """
    Get trade web page.
    """
    html = session.get(URL_TRADE, verify=True, headers={'User-Agent': UA})
    return BeautifulSoup(html.content, 'lxml')


def parse_table(soup):
    bet_task = []
    for rows in soup.find_all('tr')[1:]:
        cols = rows.find_all('td')
        # в атрибут текст передаем стоимость ставки в str
        link: dict = rows.find('button', text=re.compile('9.9'), class_='newbet')

        # if not links:
        #     linkBet = 'http://ya.ru'
        # else:
        #     for link in links:
        url_bet: str = URL_BASE + link['href']

        bet_task.append({
            'number': cols[0].strong.text,
            'city_out': cols[6].strong.text + ' ' + cols[7].strong.text + ' | ' + cols[4].strong.text,
            'city_in': cols[8].strong.text + ' | ' + cols[3].strong.text,
            'url_bet': url_bet,
        })

    count = 0

    f = open(os.path.join(script_dir, 'config/city.txt'), 'r', encoding='utf-8')
    city = f.read().split(', ')
    f.close()

    f = open(os.path.join(script_dir, 'logs/GOOD_bet.txt'), 'w', encoding='utf-8')
    f.write('Взятые заявки на \n<b>' + datetime.today().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3] + '</b>\n\n')
    f.close()
    
    for j in range(len(city)):
        cityRe = r"%s\b" % city[j]
        for i in range(len(betTask)):
            if (re.findall(cityRe, str(betTask[i].get('cityOut'))) == [city[j]]) or (re.findall(cityRe, str(betTask[i].get('cityIn'))) == [city[j]]):
                if count < config.sumBet:
                    urlBet = str(betTask[i].get('urlBet10'))

                    session.get(urlBet, verify=True, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

                    msg = '✅ <b>' + betTask[i].get('num') + '</b>\n⏺ ' + betTask[i].get('cityOut') + '\n➡️ ' + betTask[i].get('cityIn') + '\n\n'

                    f = open(os.path.join(script_dir, 'logs/GOOD_bet.txt'), 'a', encoding='utf-8')
                    f.write(msg)
                    f.close()

                    count += 1

    f = open(os.path.join(script_dir, 'logs/log_bet.txt'), 'w', encoding='utf-8')
    for i in range(len(betTask)):
        for key, value in betTask[i].items():
            f.write("{0}: {1}".format(key, value) + "\n")
        f.write("\n")
    f.close()


# def act(x):
#     return x+10
#
#
# def wait_start(runTime, action):
#     startTime = time(*(map(int, runTime.split(':'))))
#     while startTime > datetime.today().time():
#         time.sleep(1)
#     return action


def main():
    session = requests.Session()

    # wait_start('15:00:00', lambda: act(100))

    # login(session)
    soup = get_trade_page(session)
    while not soup.find('table'):
        soup = get_trade_page(session)
    parse_table(soup)
    # logout(session)


if __name__ == '__main__':
    main()
