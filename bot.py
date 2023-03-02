import logging

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from config.config import TELEGRAM_TOKEN
from db.redis_operations import db

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

START, SET_CITIES = range(2)


def start(update: Update, context: CallbackContext) -> None:
    keyboard = ReplyKeyboardMarkup([
        ['Кол-во заявок', 'Города'],
        ['Цена ставки'],
    ], resize_keyboard=True)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Вы в главном меню. Выбери функцию ⬇️',
        reply_markup=keyboard)


def quantity_tasks(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Одну", callback_data='1'),
            InlineKeyboardButton("Две", callback_data='2'),
        ],
        [
            InlineKeyboardButton("Три", callback_data='3'),
            InlineKeyboardButton("Четыре", callback_data='4'),
        ],
        [
            InlineKeyboardButton("Не брать", callback_data='0')
        ],
    ]

    qty_tasks = db.get('quantity_tasks')

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text=f'Выбери сколько заявок брать ⬇️ (кнопками снизу)'
             f'\nСейчас выбрано: {qty_tasks}',
        reply_markup=reply_markup)


def select_quantity_tasks(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    button_value = query.data

    db.replace('quantity_tasks', int(button_value))
    query.edit_message_text(text=f'Окей, возьму: {button_value}')


def get_cities(update: Update, context: CallbackContext) -> int:
    current_cities = db.get('cities')
    massage = 'Сейчас список городов такой:'
    for city in current_cities:
        massage += f'\n- {city}'
    update.message.reply_text(text=massage)
    update.message.reply_text(
        text='Чтобы изменить список, '
             'пришлите новый список городов через запятую!',
    )
    return SET_CITIES


def set_cities(update: Update, context: CallbackContext) -> int:
    cities = update.message.text.split(', ')
    db.replace('cities', cities)
    update.message.reply_text(
        text='Ок, новый список городов сохранен!'
    )
    return START


def main() -> None:
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.regex('Кол-во заявок'), quantity_tasks))
    updater.dispatcher.add_handler(CallbackQueryHandler(select_quantity_tasks))

    cities_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text('Города'), get_cities)],
        states={
            SET_CITIES: [MessageHandler(Filters.text, set_cities)]
        },
        fallbacks=[MessageHandler(Filters.text('Города'), get_cities)]
    )
    updater.dispatcher.add_handler(cities_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
