import requests
import re

pictures = []


def get_picture(id_hotels: list, count: int) -> list:

    '''
    Функция ищет фотки по ID отелей
    :param id_hotels:   ID отелей
    :param count:       Кол-во фоток
    :return:            Список с URL фото
    '''

    pictures.clear()
    try:
        for i in id_hotels:
            url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
            querystring = {"id": i}

            headers = {
                'x-rapidapi-host': "hotels4.p.rapidapi.com",
                'x-rapidapi-key': "cf825994d7mshb53d6caefe289f8p181124jsn1e81637b492b"
                }

            response = requests.request("GET", url, headers=headers, params=querystring)
            img = response.json()
            for i_num in range(count):
                string = img["hotelImages"][i_num]['baseUrl']
                result = re.sub(r'_{size}', '', string)  # Очищаем URL от _{size}
                print('URL:', result)
                pictures.append(result)
    except KeyError:
        print('Фото отеля не найдено!')
    return pictures
