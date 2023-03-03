import logging
import re
import time
from datetime import datetime
from datetime import time as dtime
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from config.config import (EFCO_LOGIN, EFCO_PASSWORD, URL_BASE, URL_LOGIN,
                           URL_LOGOUT, URL_TRADE, USER_AGENT)
from db.redis_operations import db

logger = logging.getLogger(__name__)


def login(session: requests.Session) -> None:
    """Авторизация на сайте торгов."""
    try:
        response = session.post(
            URL_LOGIN,
            params={'xLogin': EFCO_LOGIN,
                    'xPassword': EFCO_PASSWORD},
            headers={'User-Agent': USER_AGENT}
        )
    except requests.RequestException:
        logging.error('Запрос не удался')
        raise Exception('Запрос не удался')
    response.raise_for_status()


def logout(session: requests.Session) -> None:
    """Завершение сессии на сайте торгов."""
    # TODO: обложить весь код логгером
    session.get(
        URL_LOGOUT,
        headers={'User-Agent': USER_AGENT},
    )


def get_trade_page(session: requests.Session) -> BeautifulSoup:
    """
    Получение страницы торгов, возврат объекта bs4.
    """
    html = session.get(
        URL_TRADE,
        verify=True,
        headers={'User-Agent': USER_AGENT},
    )
    return BeautifulSoup(html.content, 'lxml')


def parse_table(soup: BeautifulSoup) -> List[Dict[str, str]]:
    """
    Парсинг полученного объекта soup типа bs4.
    Возвращает список словарей с необходимой информацией о заявках.
    """
    bet_tasks = []
    for rows in soup.find_all('tr')[1:]:
        cols = rows.find_all('td')
        # в атрибут text передаем стоимость ставки в str
        link: Dict = rows.find(
            'button',
            string=re.compile('9.9'),
            class_='newbet')

        if not link:
            continue
        url_bet: str = URL_BASE + str(link.get('href'))

        bet_tasks.append({
            'number_task': cols[0].strong.text,
            'departure_city': cols[4].strong.text,
            'departure_datetime': (cols[6].strong.text
                                   + ' ' + cols[7].strong.text),
            'arrival_city': cols[3].strong.text,
            'arrival_datetime': cols[8].strong.text,
            'url_bet': url_bet,
        })
    return bet_tasks


def get_cities() -> str:
    """
    Получает список городов из БД
    и возвращает подготовленную строку для RegEx операций.
    """
    return '|'.join(db.get('cities'))


def select_tasks(bet_tasks, session) -> None:
    """
    Выбор и сохранение подходящих заявок в БД.
    Предыдущие сохраненные заявки удаляются из БД.
    Запрос с выбраной заявкой на сайт торгов.
    """
    if db.get('accepted_tasks'):
        db.delete_one('accepted_tasks')
    cities: str = get_cities()
    for i in range(len(bet_tasks)):
        if re.findall(cities, str(bet_tasks[i].get('departure_city'))) \
                or re.findall(cities, str(bet_tasks[i].get('arrival_city'))):
            if count := 0 < db.get('quantity_tasks'):
                session.get(
                    str(bet_tasks[i].get('url_bet')),
                    verify=True,
                    headers={'User-Agent': USER_AGENT})
                db.rpush('accepted_tasks', bet_tasks[i])
                count += 1


def act(x):
    return x + 10


def wait_start(run_time, action):
    """Функция для 'точного' старта парсера."""
    start_time = dtime(*(map(int, run_time.split(':'))))
    while start_time > datetime.today().time():
        time.sleep(1)
    return action


def main():
    session = requests.Session()

    wait_start('15:00:00', lambda: act(100))

    login(session)
    soup = get_trade_page(session)
    while not soup.find('table'):
        soup = get_trade_page(session)
    bet_tasks = parse_table(soup)
    select_tasks(bet_tasks, session)
    logout(session)


if __name__ == '__main__':
    main()
