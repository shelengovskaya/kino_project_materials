from bs4 import BeautifulSoup
from requests import get
import time
import random
import csv

houses = []

with open('posutochno.csv', 'w') as csvfile:
    count = 1
    while count <= 100:
        # https://apartlux.ru/?page=2#apartment-sort
        url = 'https://apartlux.ru/?page=' + str(count) + '#apartment-sort'
        response = get(url)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        # <div class="home-apartments home-border">
        # <div class="cell">
        house_data = html_soup.find('div', class_='home-apartments home-border').findAll('div', class_='cell')
        if house_data != []:
            houses.extend(house_data)
            value = random.random()
            scaled_value = 1 + (value * (9 - 5))
            time.sleep(scaled_value)
        else:
            break
        count += 1

    fieldnames = ['title', 'address', 'price', 'count_rooms', 'floor', 'type_obj', 'square', 'publication_date', 'link',
                  'images', 'metro', 'phone']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    n = int(len(houses)) - 1
    # print(n)
    count = 0
    while count <= n:
        try:
            info = houses[int(count)]
            # print(info)
            # print(houses)
            # title = info.find('p', {"class":"OffersSerpItem__description"}).text
            # print(title)

            ##### адрес и метро
            # <div class="top">
            address = info.find('div', class_='top')
            # print(address)
            address = address.find('div', class_='address')
            # print(address)
            address = address.find('a', class_='gray-text')
            # print(address)
            metro = address.find('span', class_='mobile').text
            address = address.text
            address = address.replace(metro, "")
            # print(address)
            if (len(metro) > 3):
                metro = metro
                # print(metro)
            else:
                # print("no information")
                metro = "no information"
            #### телефон

            phone = info.find('div', itemprop='offers')
            # print(phone)
            phone = phone.find('div', class_='icos')
            # print(phone)
            phone = phone.find('div', class_='right mobile')
            # print(phone)
            phone = phone.find('a')
            # print(phone)
            # phone = phone.replace("+7", "kek")
            # print(phone)
            phone = phone.get('href')
            # print(phone)
            s = ""
            for i in range(len(phone) - 4):
                s += phone[i + 4]
            # print(s)
            real_phone = s

            #### link
            link = info.find('div', class_='pic')
            # print(link)
            # print()
            link = link.find('a')
            # print(link)
            link = link.get('href')
            link = 'https://apartlux.ru' + link
            # print(link)

            #### ЗАХОДИМ ВНУТРЬ
            response = get(link)
            html_soup = BeautifulSoup(response.text, 'html.parser')

            #### title
            title = html_soup.find('div', itemtype='http://schema.org/Product')
            title = title.find('h1', itemprop='name').text
            # print(title)

            #### rooms
            descr = html_soup.find('div', itemprop='description').text.split('\n')
            rooms = descr[2].split(': ')[1]
            # print(rooms)

            #### floor
            floor = descr[5].split(': ')[1]
            #### square
            square = descr[6].split(': ')[1]

            #### price

            price = html_soup.find('div', class_='grid gray-text')
            price = price.find('span', itemprop='price').text

            #### images
            images = []
            # img = html_soup.find('img', class_='tns-lazy-img loaded tns-complete')
            # img = html_soup.findAll('img', itemprop='image')
            # img = img[0].get('data-src')
            # img = 'https://apartlux.ru' + img
            # print(img)

            for img in html_soup.findAll('img', itemprop='image'):
                img = img.get('data-src')
                img = 'https://apartlux.ru' + img
                images.append(img)
            # print(images)
            type_obj = 'no information'
            publication_date = 'no information'
            csv_table = {'title': title, 'address': address, 'price': price, 'count_rooms': rooms, 'floor': floor,
                         'type_obj': type_obj, 'square': square, 'publication_date': publication_date, 'link': link,
                         'images': images, 'metro': metro, 'phone': real_phone}
            writer.writerow(csv_table)

            # print("\n")
        except AttributeError or IndexError:
            pass
        count += 1
