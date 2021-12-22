import datetime

import telebot
from telebot import types

from timetable import get_timetable, make_answer

token = "5034834018:AAGgMsUjSm7GysFae6nldhBEVMfzNfTD5x8"

bot = telebot.TeleBot(token)

kb = types.ReplyKeyboardMarkup()
commands = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница',
            'Расписание на текущую неделю',
            'Расписание на следующую неделю']
for command in commands:
    kb.row(command)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Здравствуйте! С помощью этого бота вы можете узнать актуальное расписание:',
                     reply_markup=kb)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'С помощью этого бота вы можете:\n'
                                      '/week - узнать четность текущей недели\n'
                                      '/mtuci - получить ссылку на официальный сайт МТУСИ\n'
                                      'Узнать расписание (с помощью кнопок на клавиатуре)', reply_markup=kb)


@bot.message_handler(commands=['week'])
def week_(message):
    week = datetime.datetime.now().isocalendar()[1]
    if week % 2 == 0:
        bot.send_message(message.chat.id, 'Сейчас четная неделя')
    else:
        bot.send_message(message.chat.id, 'Сейчас нечетная неделя')


@bot.message_handler(commands=['mtuci'])
def select_fairy(message):
    bot.send_message(message.chat.id, 'Официальный сайт МТУСИ - https://mtuci.ru/')


@bot.message_handler(content_types=['text'])
def timetable(message):
    if message.text in commands:
        bot.send_message(message.chat.id, make_answer(get_timetable(message)))
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')


bot.polling()
