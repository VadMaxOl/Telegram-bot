import datetime
import requests
from typing import Any

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "cf825994d7mshb53d6caefe289f8p181124jsn1e81637b492b"
    }


def search_hotels(search_city: str, count: int, status_price: str, prices: Any, distances: Any) -> Any:

    '''
    Функция по следующим данным от пользователя ищет отели.
    :param search_city:     передается название города (английскими буквами)
    :param count:           передается кол-во отелей
    :param status_price:    статус поиска отелей по ценам (дешевые, дорогие, опционально)
    :param prices:          диапазон цен для поиска отелей, если status_price = выбран опционально
    :param distances:       дистанция от центра города, если status_price = выбран опционально
    :return:                название локации, название отеля, адрес, расстояние от центра, цена за сутки
                            отдельно возвращаем ID отелей для поиска фото и название отелей для вывода перед фото
    '''

    # www. Ищем ID города, введенного пользователем
    url1 = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": search_city, "locale": "en_US"}
    response = requests.request("GET", url1, headers=headers, params=querystring)
    city_list = response.json()
    city_id = []
    print('Статус цены:', status_price)
    for i_el in city_list["suggestions"]:
        for i in (i_el['entities']):
            if search_city == i['name']:
                print('Город:', i['name'])
                city_id.append(i['destinationId'])
            else:
                break
    print('ID локации города', search_city, ':', city_id)

    # 2. Ищем ID отелей по условию status_price (дешевые, дорогие, опционально)
    url2 = "https://hotels4.p.rapidapi.com/properties/list"
    hotels = []

    for i_district in city_id:

        if status_price == 'low':
            querystring = {"destinationId": i_district, "pageNumber": "www", "pageSize": "8", "checkIn": "2020-01-08",
                           "checkOut": "2020-01-15", "adults1": "www", "sortOrder": "PRICE", "locale": "en_US",
                           "currency": "USD"}
        elif status_price == 'high':
            querystring = {"destinationId": i_district, "pageNumber": "www", "pageSize": "8", "checkIn": "2020-01-08",
                           "checkOut": "2020-01-15", "adults1": "www", "sortOrder": "PRICE_HIGHEST_FIRST",
                           "locale": "en_US", "currency": "USD"}
        elif status_price == 'optional':
            print('Начальная цена', prices[0])
            print('Конечная цена', prices[1])
            querystring = {"destinationId": i_district, "pageNumber": "www", "pageSize": "20", "checkIn": "2020-01-08",
                           "checkOut": "2020-01-15", "adults1": "www", "priceMin": prices[0],
                           "priceMax": prices[1], "locale": "en_US", "currency": "USD",
                           "landmarkIds": "15 miles"}
        response = requests.request("GET", url2, headers=headers, params=querystring)
        value_list1 = response.json()
        try:
            hotels.append(value_list1["data"]["body"]["searchResults"]["results"])
        except KeyError:
            print('В этом районе нет отелей соответствующих условиям поиска')
    print()

    print('Найденные отели по локации: ')
    hotels_id = []
    hotels_distance = []
    for i in hotels:
        for i_hotel in i:
            if status_price == 'optional':
                if (float(i_hotel['landmarks'][0]['distance'].split(' ')[0])
                    > float(distances[0])) and (float(i_hotel['landmarks'][0]['distance'].split(' ')[0]) <
                                                float(distances[1])):
                    hotels_id.append(i_hotel['id'])
                    hotels_distance.append(i_hotel['landmarks'][0]['distance'])
            else:
                hotels_id.append(i_hotel['id'])
                hotels_distance.append(i_hotel['landmarks'][0]['distance'])
        #print(i)
    print('ID отелей:', hotels_id)
    print(hotels_distance)
    dist = []
    for i in hotels_distance:
        dist.append(i.split(' ')[0])
    print(dist)
    print()

    # 3. Ищем информацию по каждому отелю
    total = []
    hotels_names = []
    hotels_id_list = list(hotels_id)
    try:
        for i in range(0, int(count)):
            i_id = hotels_id_list[i]
            querystring = ({"id": i_id, "checkIn": "2020-01-08", "checkOut": "2020-01-15", "adults1": "www",
                            "currency": "USD", "locale": "en_US"})
            url3 = "https://hotels4.p.rapidapi.com/properties/get-details"
            response1 = requests.request("GET", url3, headers=headers, params=querystring)
            value_list = response1.json()
            location = (value_list['data']['body']["pdpHeader"]["hotelLocation"]["locationName"])
            hotel = (value_list['data']['body']['propertyDescription']["name"])
            address = (value_list['data']['body']['propertyDescription']["address"]["fullAddress"])
            distance = 'Расстояние от центра:'
            price = (value_list['data']['body']['propertyDescription']["featuredPrice"]["currentPrice"]['formatted'])
            emptiness = (' ')
            hotels_names.append(hotel)
            total.extend([location, hotel, address, distance, hotels_distance[i], price, emptiness])
        print(total)
        with open('history.log ', 'a', encoding='UTF-8') as file:
            file.write('\n ' + str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) +
                       '\nОтели: '+'\n' + "\n".join(total))
        return ["\n".join(total), hotels_id, hotels_names]

    except IndexError:
        return 'Введен не существующий город или нет отелей соответствующих условиям поиска'
