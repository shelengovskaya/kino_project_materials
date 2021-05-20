from bs4 import BeautifulSoup
from requests import get
import time
import random
import csv

houses = []

with open('move.csv', 'w') as csvfile:
    count = 1
    while count <= 100:
        url = 'https://move.ru/kvartiry_na_sutki/?page=' + str(count) + '&limit=30'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')

        house_data = html_soup.find('div', class_='container main items-page').findAll('div',
                                                                                       class_='search-item move-object')
        if house_data != []:
            houses.extend(house_data)
            value = random.random()
            scaled_value = 1 + (value * (9 - 5))
            time.sleep(scaled_value)
        else:
            break
        count += 1

    fieldnames = ['title', 'address', 'price', 'count_rooms', 'floor', 'type_obj', 'square', 'publication_date', 'link',
                  'images']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    n = int(len(houses)) - 1
    count = 0
    while count <= n:  # count <= n
        try:
            info = houses[int(count)]

            title = info.find('a', {"class": "search-item__title-link search-item__item-link"}).text

            link = 'https:' + info.find('a', {"class": "search-item__title-link search-item__item-link"}).get('href')
            response = get(link)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            with open('out.txt', 'w') as f:
                f.write(str(html_soup))

            # IMAGES
            images = []
            for img in html_soup.find('div',
                                      class_='images-slider_fotorama js-fotorama-init images-slider__fotorama-only-slides').findAll(
                    'a'):
                images.append(img.get('href'))

            # INFO

            details = html_soup.findAll('ul', class_='object-info__details-table')

            info = details[0].findAll('div', class_='object-info__details-table_property_value')
            price = info[0].text
            count_rooms = info[2].text
            floor = info[3].text
            type_obj = info[4].text

            info = details[1].findAll('div', class_='object-info__details-table_property_value')
            square = info[0].text
            publication_date = info[3].text

            info = details[4].findAll('div', class_='object-info__details-table_property_value')
            address = info[0].text

            csv_table = {'title': title, 'address': address, 'price': price, 'count_rooms': count_rooms, 'floor': floor,
                         'type_obj': type_obj, 'square': square, 'publication_date': publication_date, 'link': link,
                         'images': images}

            writer.writerow(csv_table)


        except AttributeError or IndexError:
            pass

        count += 1