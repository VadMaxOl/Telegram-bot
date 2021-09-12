import requests

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "64d58aac67mshd1bdc2e7b1ee572p14febdjsnfc859fb33ffd"
    }


def search_lowprice(search_city, count):
    url1 = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": search_city, "locale": "en_US"}
    response = requests.request("GET", url1, headers=headers, params=querystring)
    city_list = response.json()
    city_id = []
    #print(city_list["suggestions"])
    for i_el in city_list["suggestions"]:
        for i in (i_el['entities']):
            city_id.append(i['destinationId'])
    print('ID районов города', search_city, ':', city_id)

    url2 = "https://hotels4.p.rapidapi.com/properties/list"
    hotels = []
    count_district = len(city_id)
    for i_district in city_id:
        querystring = {"destinationId": i_district, "pageNumber": "1", "pageSize": "1", "checkIn": "2020-01-08",
                       "checkOut": "2020-01-15", "adults1": "1", "sortOrder": "PRICE", "locale": "en_US",
                       "currency": "USD"}
        response = requests.request("GET", url2, headers=headers, params=querystring)
        value_list1 = response.json()
        print('Осталось проверить районов: ', count_district)
        #print(value_list1)
        try:
            hotels.append(value_list1["data"]["body"]["searchResults"]["results"])
        except KeyError:
            print('В этом районе нет отелей соответствующих условиям поиска')
        count_district -= 1
    #print('Отели', hotels)
    print()

    print('Найденные отели по районам: ')
    hotels_id = []
    for i in hotels:
        hotels_id.append(i[0]['id'])
        print(i)
    hotels_id = set(hotels_id)
    print('ID отелей:', hotels_id)
    print()

    total = []
    count_hotels_temp = 0
    print(count)
    for i_id in hotels_id:
        if count_hotels_temp == count:
            break
        else:
            querystring = ({"id": i_id, "checkIn": "2020-01-08", "checkOut": "2020-01-15", "adults1": "1",
                            "currency": "USD", "locale": "en_US"})
            url3 = "https://hotels4.p.rapidapi.com/properties/get-details"
            response1 = requests.request("GET", url3, headers=headers, params=querystring)
            value_list = response1.json()
            location = (value_list['data']['body']["pdpHeader"]["hotelLocation"]["locationName"])
            hotel = (value_list['data']['body']['propertyDescription']["name"])
            address = (value_list['data']['body']['propertyDescription']["address"]["fullAddress"])
            price = (value_list['data']['body']['propertyDescription']["featuredPrice"]["currentPrice"]['formatted'])
            emptiness = (' ')
            count_hotels_temp += 1
            total.extend([location, hotel, address, price, emptiness])
            print(count_hotels_temp)
    print(total)
    return "\n".join(total)
