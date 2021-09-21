"""
Дипломный проект. Telegram-бот для сайта: Hotels.com компании Too Easy Travel.
Автор: Байбеков Вадим Альбертович.
Название бота в Telegram: VENOM_newbot
"""

# Чтобы запустить бота: напишите в терминале "python main.py"
# Чтобы остановить бота: нажмите Ctrl+C и подождите

import datetime
import telebot
from hotels import search_hotels
from foto import get_picture
from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot_token = os.environ.get("token")
bot = telebot.TeleBot(bot_token)


@bot.message_handler(content_types=["text", "document", "photo"])
def get_text_messages(message):
    """
    Функция отвечает за диалог с пользователем
    и за получение команд и входных данных от него
    """
    if message.text == "Привет" or message.text == "привет":
        logging(message.text)
        bot.send_message(message.chat.id, "Привет, {0.first_name}!".format(message.from_user, bot.get_me()))
        bot.send_message(message.chat.id, "Чем я могу вам помочь?"
                                          "\n Существующие команды:"
                                          "\n /lowprice - поиск самых дешёвых отелей в городе"
                                          "\n /highprice - поиск самых дорогих отелей в городе"
                                          "\n /bestdeal - отели, оптимальные по цене и расположению"
                                          "\n /history - получить историю поиска отелей")

    elif message.text == "/help":
        logging(message.text)
        bot.send_message(message.chat.id, "Напишите Привет")
    elif message.text == "/hello_world":
        logging(message.text)
        bot.send_message(message.chat.id, "Это Telegram-бот по поиску отелей. Автор Байбеков Вадим Альбертович")
    elif message.text == "/lowprice":
        logging(message.text)
        bot.send_message(message.chat.id, "Введите название города английскими буквами (пример: las vegas)")
        bot.register_next_step_handler(message, get_city)
        global status_price
        status_price = 'low'
    elif message.text == "/highprice":
        logging(message.text)
        bot.send_message(message.chat.id, "Введите название города английскими буквами (пример: boston)")
        bot.register_next_step_handler(message, get_city)
        status_price = 'high'
    elif message.text == "/bestdeal":
        logging(message.text)
        bot.send_message(message.chat.id, "Введите название города английскими буквами (пример: miami)")
        bot.register_next_step_handler(message, get_city)
        status_price = 'optional'
    elif message.text == "/history":
        with open('history.log ', 'r', encoding='UTF-8') as file:
            bot.send_document(message.chat.id, file)
    else:
        logging(message.text)
        bot.send_message(message.chat.id, "Я вас не понимаю. Напишите /help или /hello_world.")


def get_city(message):  # получаем название города
    global city
    city = message.text
    logging(message.text)
    city = (city.title())
    bot.send_message(message.chat.id, 'Введите кол-во отелей (не более 8)')
    print(city)
    bot.register_next_step_handler(message, get_count_hotels)


def get_count_hotels(message):  # получаем кол-во отелей
    global count_hotels
    count_hotels = message.text
    logging(message.text)
    print(count_hotels)
    if int(count_hotels) > 8:  # По ТЗ определяем заранее определенный максимум в 8 отелей
        bot.send_message(message.chat.id, "Вы ввели больше 8 отелей. Хотите сломать программу?! :)")
        bot.send_message(message.chat.id, "Тогда начинаем заново. Напишите: 'привет'")
    else:
        if status_price == 'optional':
            bot.send_message(message.chat.id, 'Введите диапазон цен через дефис (пример: 10-40)')
            bot.register_next_step_handler(message, get_price)
        else:
            optional_price = None
            optional_distance = None
            value = search_hotels(city, count_hotels, status_price, optional_price, optional_distance)
            bot.send_message(message.chat.id, value)
            if value == 'Введен не существующий город или нет отелей соответствующих условиям поиска':
                bot.send_message(message.chat.id, "Тогда начинаем заново. Напишите: 'привет'")
            else:
                global hotels
                hotels = value[1]  # Получаем ID отелей для поиска фото
                global hotels_names
                hotels_names = value[2]  # Получаем названия отелей для вывода клиенту перед фото
                print(hotels_names)
                bot.send_message(message.chat.id, 'Вы хотите увидеть фото выбранных отелей? (пример: да)')
                bot.register_next_step_handler(message, get_img)


def get_price(message):  # диапазон цен для поиска отелей, если status_price = выбран опционально
    global optional_price
    price = message.text
    logging(message.text)
    optional_price = price.split('-')
    print('Диапазон цен:', optional_price)
    if float(optional_price[0]) > float(optional_price[1]):
        bot.send_message(message.chat.id, "Вообще то первое число должно быть меньше второго. "
                                          "Хотите сломать программу?! :)")
        bot.send_message(message.chat.id, "Тогда начинаем заново. Напишите: 'привет'")
    else:
        bot.send_message(message.chat.id, 'Введите диапазон расстояния отеля от центра'
                                          ' через дефис (пример: 5-20)')
        bot.register_next_step_handler(message, get_distance)


def get_distance(message):  # дистанция от центра города, если status_price = выбран опционально
    global optional_distance
    distance = message.text
    logging(message.text)
    optional_distance = distance.split('-')
    print('Диапазон расстояния от центра города:', optional_distance)
    if float(optional_distance[0]) > float(optional_distance[1]):
        bot.send_message(message.chat.id, "Вообще то первое число должно быть меньше второго. "
                                          "Хотите сломать программу?! :)")
        bot.send_message(message.chat.id, "Тогда начинаем заново. Напишите: 'привет'")
    else:
        value = search_hotels(city, count_hotels, status_price, optional_price, optional_distance)
        bot.send_message(message.chat.id, value)
        global hotels
        hotels = value[1]  # Получаем ID отелей для поиска фото
        global hotels_names
        hotels_names = value[2]  # Получаем названия отелей для вывода клиенту перед фото
        print(hotels_names)
        bot.send_message(message.chat.id, 'Вы хотите увидеть фото выбранных отелей? (пример: нет)')
        bot.register_next_step_handler(message, get_img)


def get_img(message):  # получаем ответ, нужны фотки отелей или нет
    answer = message.text
    logging(message.text)
    if answer == "Да" or answer == "да":
        bot.send_message(message.chat.id,
                         'Сколько фото вы хотите увидеть по каждому отелю (не более 3)? (пример: 2)')
        bot.register_next_step_handler(message, get_count_picture)
    else:
        print('Программа начинается заново')
        bot.send_message(message.chat.id, "Тогда начинаем заново. Напишите: 'привет'")


def get_count_picture(message):  # узнаем, сколько нужно фоток
    global count_picture
    count_picture = message.text
    logging(message.text)
    if int(count_picture) > 3:  # По ТЗ определяем заранее определенный максимум в 3 фотки
        bot.send_message(message.chat.id, "Вы ввели больше 3 фото. Хотите сломать программу?! :)")
        bot.send_message(message.chat.id, "Тогда начинаем заново. Напишите: 'привет'")
    else:
        value_picture = get_picture(hotels[:int(count_hotels)], int(count_picture))
        print(value_picture)
        # Код ниже нужен, для вывода названий отелей перед фотками
        count_name = 0
        count = 0
        bot.send_message(message.from_user.id, hotels_names[count_name])
        for i_pic in value_picture:
            if count == int(count_picture):
                count_name += 1
                bot.send_message(message.chat.id, hotels_names[count_name])
                count = 0
            bot.send_photo(message.chat.id, i_pic)
            count += 1


def logging(message):  # Функция записи всех команд в лог
    with open('history.log ', 'a', encoding='UTF-8') as file:
        file.write('\n ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + '   Команда: ' + message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
