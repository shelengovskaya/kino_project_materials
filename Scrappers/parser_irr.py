from bs4 import BeautifulSoup
from requests import get
import time
import random
import csv

houses = []

with open('irr.csv', 'w') as csvfile:
    count = 1
    while count <= 10:
        try:
            url = 'https://irr.ru/real-estate/rent/page' + str(count)

            try:
                response = get(url)
            except Exception as exc:
                print('Error: ', exc)

            html_soup = BeautifulSoup(response.text, 'html.parser')

            house_data = html_soup.find('div', class_='js-listingContainer').findAll('div',
                                                                                     class_='listing__item js-productBlock')

            if house_data != []:
                houses.extend(house_data)
                value = random.random()
                scaled_value = 1 + (value * (9 - 5))
                time.sleep(scaled_value)
            else:
                break
            count += 1
        except AttributeError or TypeError:
            break

    fieldnames = ['title', 'address', 'price', 'count_rooms', 'floor', 'type_obj', 'square', 'publication_date', 'link',
                  'images']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    n = int(len(houses)) - 1
    count = 0
    while count <= n:
        try:
            title = address = price = count_rooms = floor = type_obj = square = publication_date = link = ''

            info = houses[int(count)]

            link = info.get('data-href')
            response = get(link)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            # IMAGES
            images = []
            for img in html_soup.find('div', class_='lineGallery js-lineProductGallery').findAll('img'):
                images.append(img.get('data-src'))

            # INFO

            square = info.find('div', class_='listing__itemColumn listing__itemColumn_param1').text
            floor = info.find('div', class_='listing__itemColumn listing__itemColumn_param2').text[4:]

            price = html_soup.find('div', class_='productPage__price').text.strip()

            details = html_soup.find('div', class_='productPage js-productPageDescriptions')

            title = html_soup.find('h1', class_='productPage__title js-productPageTitle').text.strip()

            info = details.find('div',
                                class_='productPage__characteristicsBlock js-productPage__characteristicsBlock').findAll(
                'span', class_='productPage__characteristicsItemValue')

            count_rooms = info[0].text
            type_obj = 'квартира'
            publication_date = html_soup.find('div', class_='productPage__createDate').text.strip()
            address = html_soup.find('div', class_='productPage__infoTextBold js-scrollToMap').text.strip()

            csv_table = {'title': title, 'address': address, 'price': price, 'count_rooms': count_rooms, 'floor': floor,
                         'type_obj': type_obj, 'square': square, 'publication_date': publication_date, 'link': link,
                         'images': images}

            writer.writerow(csv_table)

        except AttributeError or IndexError:
            pass

        count += 1