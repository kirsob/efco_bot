import telebot
from telebot import apihelper
from telebot import types
from config import config
from config import bdworker

#apihelper.proxy = {'https':'socks5h://4009548:mYlbBtTn@orbtl.s5.opennetwork.cc:999'}
#apihelper.proxy = {'https':'socks5h://aTKWx66aHl:TLcSITj70x@172.96.139.225:29519'}
apihelper.proxy = {'http':'socks5://localhost:9050'}

TOKEN = '983071785:AAE-4gKtJpp7PA1wLtcXUtdvUz9duTP1BnA'

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
@bot.message_handler(regexp="Назад")
def command_handler(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    edit_city = types.KeyboardButton('Список городов')
    bet = types.KeyboardButton('Кол-во заявок')
    what = types.KeyboardButton('Что взял?')

    markup.add(edit_city, bet, what)

    bdworker.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, 'Выбери функцию ⬇️', reply_markup=markup)

@bot.message_handler(commands=['help'])
def echo_help(message):
    msg = '<b>Помощь по ЭФКА-бот:</b>\n✅️Список городов - раздел для изменения списка городов\n✅️Кол-во заявок - раздел для изменения количества заявок которые будут взяты\n✅Что взял? - раздел позволяющий увидеть какие заявки успешно взяты (обновляется после 15:30)\n\n❗️Если бот не отвечает попробуй его перезагрузить командой /start'
    bot.send_message(message.chat.id, msg, parse_mode='HTML')

@bot.message_handler(regexp="Что взял?")
@bot.edited_message_handler(regexp="Что взял?")
def echo_what(message):
    f = open('logs/GOOD_bet.txt', 'r')
    msg = f.read()
    f.close()

    bot.send_message(message.chat.id, msg, parse_mode='HTML')
    command_handler(message)

@bot.message_handler(regexp="Кол-во заявок")
@bot.edited_message_handler(regexp="Кол-во заявок")
def echo_bet(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    one = types.KeyboardButton('1')
    two = types.KeyboardButton('2')
    three = types.KeyboardButton('3')
    four = types.KeyboardButton('4')
    no = types.KeyboardButton('Не брать')
    exit = types.KeyboardButton('Назад')

    markup.add(one, two, three, four, no, exit)

    f = open('config/bet_num.txt', 'r')
    msg = f.read()
    f.close()

    bot.send_message(message.chat.id, 'Выбери сколько заявок брать ⬇️ (только кнопками снизу)', parse_mode='HTML', reply_markup=markup)
    if msg != '0':
        bot.send_message(message.chat.id, 'Текущее кол-во заявок: <b>' + msg + '</b>', parse_mode='HTML')

    @bot.message_handler(regexp="1")
    @bot.message_handler(regexp="2")
    @bot.message_handler(regexp="3")
    @bot.message_handler(regexp="4")
    def echo_bet_num(message):
        f = open('config/bet_num.txt', 'w')
        f.write(message.text)
        f.close()

        bot.send_message(message.chat.id, 'Новое кол-во заявок: <b>' + message.text + '</b>. Постараюсь взять, если столько будет', parse_mode='HTML')
        command_handler(message)

    @bot.message_handler(regexp="Не брать")
    def echo_bet_num_null(message):
        f = open('config/bet_num.txt', 'w')
        f.write('0')
        f.close()

        bot.send_message(message.chat.id, 'Ок, не буду брать заявки, пока ты не напишешь новое кол-во заявок', parse_mode='HTML')
        command_handler(message)

@bot.message_handler(regexp="Список городов")
@bot.edited_message_handler(regexp="Список городов")
def echo_city(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    exit = types.KeyboardButton('Назад')

    markup.add(exit)

    f = open('config/city.txt', 'r')
    city = f.read()
    f.close()

    bot.send_message(message.chat.id, 'Напиши новый список в необходимой последовательности (предыдущий список будет удален!)\nПример написания: <b>Краснодар, Анапа, Крымск, Томск</b>\nЕсли напишешь без запятых или с маленькой буквы - все сломаешь', parse_mode='HTML')
    bot.send_message(message.chat.id, 'Текущий список: <b>' + city + '</b>', reply_markup=markup, parse_mode='HTML')
    bdworker.set_state(message.chat.id, config.States.S_CITY.value)

@bot.message_handler(func=lambda message: bdworker.get_current_state(message.chat.id) == config.States.S_CITY.value)
def echo_edit(message):
    if message.text:
        f = open('config/city.txt', 'w')
        f.write(message.text)
        f.close()
    bot.send_message(message.chat.id, 'Запомнил: <b>' + message.text + '</b>', parse_mode='HTML')
    bdworker.set_state(message.chat.id, config.States.S_START.value)
    command_handler(message)

@bot.message_handler(regexp="Logs")
def echo_bet_num_null(message):
    f = open('logs/log_bet.txt', 'rb')

    bot.send_document(message.chat.id, f)
    f.close()
    command_handler(message)

def main():
    bot.polling(none_stop=True, timeout=123)

if __name__ == '__main__':
    main()
