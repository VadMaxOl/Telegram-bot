"""
Дипломный проект. Telegram-бот для сайта: Hotels.com компании Too Easy Travel.
Автор: Байбеков Вадим Альбертович.
Название бота в Telegram: VENOM_newbot
"""

# Чтобы запустить бота: напишите в терминале "python main.py"
# Чтобы остановить бота: нажмите Ctrl+C и подождите

import requests
import config
import telebot
from lowprice import search_lowprice
from telebot import types
from telebot.types import InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?"
                                               "\n Существующие команды:"
                                               "\n /lowprice - поиск самых дешёвых отелей в городе"
                                               "\n /highprice - поиск самых дорогих отелей в городе"
                                               "\n /bestdeal - отели, оптимальные по цене и расположению"
                                               "\n /history - просмотреть историю поиска отелей")

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    elif message.text == "/hello_world":
        bot.send_message(message.from_user.id, "Я Telegram-бот. Мой автор: Байбеков Вадим Альбертович")
    elif message.text == "/lowprice":
        bot.send_message(message.from_user.id, "Введите название города")
        bot.register_next_step_handler(message, get_city)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help или /hello_world.")


def get_city(message):  # получаем название города
    global city
    city = message.text
    bot.send_message(message.from_user.id, 'Введите кол-во отелей')
    print(city)
    bot.register_next_step_handler(message, get_count_hotels)


def get_count_hotels(message):
    global count_hotels
    count_hotels = message.text
    print(count_hotels)
    value = search_lowprice(city, count_hotels)
    bot.send_message(message.from_user.id, value)
    #bot.register_next_step_handler(message, searching)

'''
def searching(message):
    print(city)
    print(count_hotels)
    bot.send_message(message.from_user.id, search_lowprice(city, count_hotels))
'''

if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
