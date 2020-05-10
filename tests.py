import sys
from math import *
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image
from geo import map_size
from random import shuffle
from PIL import ImageFont, ImageDraw

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
print('Напишите название города')
cities = ['ульяновск', 'казань', 'самара', 'москва', 'санкт-петербург', 'калининград']
d = {'ульяновск': ['ул. Нариманова, 7', 'ул. Гончарова, 21', 'Президентский мост'],
     'казань': ['Казанский Кремль', 'ул. Федосеевская, 36', 'ул. Каюма Насыри', 'ул. Старо-Аракчинская, 4'],
     'самара': ['Комсомольская площадь, 1', 'проспект Ленина, 21', 'ул. Фрунзе, 167', 'Площадь Куйбышева, 1'],
     'москва': ['Комсомольская площадь, 2', 'Московский Кремль', 'Ленинские горы, 1', 'ул. Мясницкая, 20'],
     'санкт-петербург': ['Дворцовая площадь, 2', 'Набережная канала Грибоедова, 2', 'Петропавловская крепость'],
     'калининград': ['ул. Канта, 1', 'ул. Маршала Василевского', 'остров Октябрьский']}
city = input().strip()
while city.lower() not in cities:
    city = input('Такого города пока нет в базе\n').strip()
city = city.lower()
shuffle(d[city])
toponyms = d[city]
for i in toponyms:
    toponym_to_find = " ".join('{}, {}'.format(city, i))

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        # обработка ошибочной ситуации
        pass

    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    toponym_size = map_size(toponym)

    ######################################

    address_ll = toponym_longitude + ',' + toponym_lattitude


    # Получаем первую найденную организацию.
    # Название организации.
    delta = '0.005'
    map = ['sat', 'map']
    shuffle(map)
    map_params = {
        "l": "{},skl".format(map[0]),
        "ll": address_ll,
        "z": 16
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    # ... и выполняем запрос
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(
        response.content)).show()

    print('Для показа следующей фото напишите next')
    next = ''
    while not next:
        next = input()
        pass
    next = ''

# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы