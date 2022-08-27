# -*- coding: utf-8 -*-
import requests
from config import config
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime, time
from time import sleep
import os

script_dir = os.path.dirname(__file__)

session = requests.Session()

def parser():

    #url = "http://y91805lt.beget.tech/index.html"
    url = "https://taman.trans.efko.ru/trade/2"
    urlAuth = "https://taman.trans.efko.ru/login.php"
    urlLogout = "https://taman.trans.efko.ru/logout.php"
    urlBet = "https://taman.trans.efko.ru"

    betTask = []
    i=0

    session.post(urlAuth, config.data, verify=True, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    html = session.get(url, verify=True, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(html.content, 'lxml')

    while soup.find('table') == None:
        html = session.get(url, verify=True, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})
        soup = BeautifulSoup(html.content, 'lxml')
        i += 1

    for rows in soup.find_all('tr')[1:]:
        cols = rows.find_all('td')

        links = rows.find_all('button', text=re.compile("11"), class_='newbet')
        linkBet = None

        if not links:
            linkBet = 'http://ya.ru'
        else:
            for link in links:
                linkBet = urlBet + link.get('href')
        #print(linkBet)

        betTask.append({
            'num': cols[0].strong.text,
            'cityOut': cols[6].strong.text + ' ' + cols[7].strong.text + ' | ' + cols[4].strong.text,
            'cityIn': cols[8].strong.text + ' | ' + cols[3].strong.text,
            'urlBet10': linkBet
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


    session.get(urlLogout, verify=True, headers={'User-Agent': UserAgent(verify_ssl=False).chrome})

    f = open(os.path.join(script_dir, 'logs/log_bet.txt'), 'w', encoding='utf-8')
    for i in range(len(betTask)):
        for key, value in betTask[i].items():
            f.write("{0}: {1}".format(key, value) + "\n")
        f.write("\n")
    f.close()

def act(x):
    return x+10

def wait_start(runTime, action):
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time():
        sleep(1)
    return action

def main():
    wait_start('15:00:00', lambda: act(100))
    parser()

if __name__ == '__main__':
    main()
