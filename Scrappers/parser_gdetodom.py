from bs4 import BeautifulSoup
from requests import get
import time
import random
import csv
import io

houses = []

def no_spaces(s):
    i = 0
    while s[i] == ' ' or s[i] == '\n':
        s = s[1:]
    while s[len(s)-1] == ' ':
        s = s[:-1]
    i = 1
    while i < len(s)-1:
        if s[i] == ' ' and s[i+1] == ' ':
            s = s[:i+1] + s[i+2:]
        else:
            i += 1
    return s


with io.open('gdetodom.csv', 'w', encoding="utf-8") as csvfile:
    count = 1
    while count <= 100:
        url = 'https://www.gdeetotdom.ru/snyat-kvartiru-posutochno-moskva/?page=' + str(count)
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        house_data = html_soup.find('div', class_='b-objects-list').findAll('div', class_='c-card__description')

        if house_data != []:
            houses.extend(house_data)
            value = random.random()
            scaled_value = 1 + (value * (9 - 5))
            time.sleep(scaled_value)
        else:
            break
        count += 1

    # print(count)
    print(len(houses))
    fieldnames = ['title', 'rooms', 'address', 'price', 'floor', 'square', 'publication_date', 'link',
                  'images']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    n = int(len(houses)) - 1
    count = 0
    while count <= n:  # count <= n
        try:
            info = houses[int(count)]

            title = info.find('a', class_='c-card__title').text
            link = info.find('a', class_='c-card__title').get('href')
            title = no_spaces(title)
            # print(title)
            # print(link)
            response = get(link)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            # INFO
            details = html_soup.find('div', class_='b-dotted-block__container')
            info = details.findAll('div', class_='b-dotted-block__right')

            price = info[0].find('span', class_='b-dotted-block__inner').text
            price = no_spaces(price)
            # print(price)
            floor = info[2].find('span', class_='b-dotted-block__inner').text
            # print(floor)
            rooms = info[3].find('span', class_='b-dotted-block__inner').text
            # print(rooms)
            square = info[4].find('span', class_='b-dotted-block__inner').text
            # print(square)

            details = html_soup.find('div', class_='address-params')
            info = details.findAll('div', class_='b-dotted-block__right')

            address = ""
            address += info[0].find('a', class_='linking').text + ', '
            address += info[1].find('a', class_='linking').text + ', '
            address += info[2].find('a', class_='linking').text + ', '
            address += info[3].find('a', class_='linking').text + ', '
            address += no_spaces(info[4].text)
            address = address[:len(address) - 1]

            # print(address)
            info = html_soup.find('ul', class_='activity-line')
            publication_date = info.find('li', class_='activity__publish').text

            # IMAGES
            images = []
            for img in html_soup.find('div', class_='gallery photos').findAll('img', class_='slide js-slide '):
                images.append(img.get('src'))

            csv_table = {'title': title, 'rooms': rooms, 'address': address, 'price': price, 'floor': floor,
                         'square': square, 'publication_date': publication_date, 'link': link,
                         'images': images}

            writer.writerow(csv_table)

        except AttributeError or IndexError:
            pass

        count += 1
