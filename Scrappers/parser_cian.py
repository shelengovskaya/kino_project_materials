from bs4 import BeautifulSoup
from requests import get
import time
import random
import csv
import io

houses = []

with io.open('cian.csv', 'w', encoding="utf-8") as csvfile:
    count = 1
    while count <= 100:
        url = 'https://www.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p=' + str(count) + '&region=1&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1&room7=1&room9=1&type=2'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        house_data = html_soup.find('div', class_='_93444fe79c--wrapper--E9jWb').findAll('div', class_='_93444fe79c--card--2umme _93444fe79c--promoted--62c4a')

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
    fieldnames = ['title', 'type_obj', 'address', 'price', 'floor', 'square', 'publication_date', 'link',
                  'images']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    n = int(len(houses)) - 1
    count = 0
    while count <= n:  # count <= n
        try:
            info = houses[int(count)]

            title = info.find('span', {"class":
                                           "_93444fe79c--color_primary_100--O6-gZ _93444fe79c--lineHeight_28px--3QLml _93444fe79c--fontWeight_bold--t3Ars _93444fe79c--fontSize_22px--3UVPd _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER"}).text

            link = info.find('a', {"class": "_93444fe79c--link--39cNw"}).get('href')

            price = info.find('span', class_='_93444fe79c--color_black_100--A_xYw _93444fe79c--lineHeight_28px--3QLml _93444fe79c--fontWeight_bold--t3Ars _93444fe79c--fontSize_22px--3UVPd _93444fe79c--display_block--1eYsq _93444fe79c--text--2_SER').text

            # IMAGES
            images = []
            for img in info.findAll('img', class_='_93444fe79c--image--2X3m2'):
                images.append(img.get('src'))
            response = get(link)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            # INFO
            info = html_soup.findAll('a', class_='a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr')
            address = info[0].text
            address += ', '
            address += info[1].text
            address += ', '
            address += info[2].text
            address += ', '
            address += info[3].text
            address += ', '
            address += info[4].text

            info = html_soup.find('h1', class_='a10a3f92e9--title--2Widg')
            type_obj = info.text

            info = html_soup.findAll('div', class_='a10a3f92e9--info-value--18c8R')
            details = html_soup.findAll('div', class_='a10a3f92e9--info-title--2bXM9')
            for i in range(0, len(details)):
                if details[i].text == "Общая":
                    square = info[i].text
                elif details[i].text == "Этаж":
                    floor = info[i].text

            info = html_soup.find('div', class_='a10a3f92e9--container--3nJ0d')
            publication_date = info.text

            with io.open('out.txt', "w", encoding="utf-8") as f:
                f.write(title)

            csv_table = {'title': title, 'type_obj': type_obj, 'address': address, 'price': price, 'floor': floor,
                        'square': square, 'publication_date': publication_date, 'link': link,
                         'images': images}

            writer.writerow(csv_table)

        except AttributeError or IndexError:
            pass

        count += 1
