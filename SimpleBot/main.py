import telebot
from telebot import types

from keeboards import winks, keyboards

token = "2118555279:AAGfl8HEBfjjPw6wVG-IjTe3XGWVEANahQw"

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!!! с помощью этого бота ты можешь узнать, кто ты из феечек винкс!!!!'
                                      '\nНачни проходить тест /start_test')


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет!!! с помощью этого бота ты можешь узнать, кто ты из феечек винкс!!!!'
                                      '\nНачни проходить тест /start_test'
                                      '\nИли выбери фею, о которой хочешь узнать болбше!!!! /info')


i = 0

questions = ['Какой твой любимый цвет?',
             'С кем ты бы хотел_а встречаться?',
             'Какой магией ты бы мог_ла обладать?',
             'Чем ты занимаешься в свободное время?']


@bot.message_handler(commands=['start_test'])
def q1(message):
    for fairy in winks:
        if message.text in fairy.a:
            fairy.k += 1
    global i
    bot.send_message(message.chat.id, questions[i], reply_markup=keyboards[i])
    if i < 3:
        bot.register_next_step_handler(message, q1)
        i += 1
    else:
        bot.register_next_step_handler(message, end_test)


def end_test(message):
    max_k = 0
    info = ''
    image = ''
    name = ''
    for fairy in winks:
        if fairy.k > max_k:
            max_k = fairy.k
            info = fairy.info
            image = fairy.image
            name = fairy.name

    bot.send_message(message.chat.id, f"Ты - {name} \n\n {info}", reply_markup=types.ReplyKeyboardRemove(),
                     parse_mode="Markdown")
    bot.send_photo(message.chat.id, open(f'images/{image}', 'rb'))


@bot.message_handler(commands=['info'])
def select_fairy(message):
    kb = types.ReplyKeyboardMarkup()
    for fairy in winks:
        kb.row(fairy.name)
    bot.send_message(message.chat.id, "Какая фея тебя интересует?", reply_markup=kb)
    bot.register_next_step_handler(message, print_info)


def print_info(message):
    for fairy in winks:
        if fairy.name == message.text:
            bot.send_message(message.chat.id, fairy.info, parse_mode="Markdown")


bot.polling()
