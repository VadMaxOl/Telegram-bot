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

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
    elif message.text == "/hello_world":
        bot.send_message(message.from_user.id, "Я Telegram-бот. Мой автор: Байбеков Вадим Альбертович")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help или /hello_world.")


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
