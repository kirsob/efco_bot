# Бот-система автоматической игры на торгах ЭФКО
## Установка Tor для стабильной работы Бота
```
sudo apt-get install tor
#необязательные пункты
sudo nano /etc/tor/torrc 
sudo systemctl restart tor@default.service
```

## Подготовка скрипта
Клонируем проект

```git clone git@github.com:sobkir/efco.git```

Выдаем 777 права на папку efco/ и **выставляем владельца**

```
sudo chmod -R 777 efco
sudo chown -R user:group efco
```

Устанавливаем зависимости

```
pip3 install requirements.txt
```

## Добавляем бота в systemd
Проверяем файл bot_efco.service и можно добавлять
```
sudo cp bot_efco.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable bot_efco
sudo systemctl start bot_efco
```
## Включаем крон

```
crontab -u USER -e
```
...и вставляем
```
58 14 * * 1-5 python3 ~/efco/main.py #указать полный путь
```
