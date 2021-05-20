from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
import time
import random
import csv

#### оставшиеся проблемы:
#### 1 какие-то обьявления просто пропускаются из-за AttributeError or IndexError (для всех скраперов)
#### 2 если обьявление "устарело или снято", то все равно заходит внутрь и пытается собрать инфу
#### 3 бывает несколько метро
#### 4 что-то странное с телефоном

houses = []

with open('realty_yandex.csv', 'w') as csvfile:
    count = 1
    while count <= 1:

        # url = 'https://realty.yandex.ru/moskva/snyat/kvartira/posutochno/?page=' + str(count - 1)
        # response = get(url)
        # html_soup = BeautifulSoup(response.text, 'html.parser')

        html = urlopen("https://realty.yandex.ru/moskva/snyat/kvartira/posutochno/?page=" + str(count - 1))
        html_soup = BeautifulSoup(html, "html.parser")
        # print(html_soup)
        house_data = html_soup.find('ol', class_='OffersSerp__list').findAll('li',
                                                                             class_='OffersSerpItem OffersSerpItem_view_desktop OffersSerpItem_format_full OffersSerp__list-item OffersSerp__list-item_type_offer')
        # print(house_data)

        if house_data != []:
            # print("gj")
            houses.extend(house_data)
        # print(houses)

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

            title = 'no infromation'
            title = info.find('p', {"class": "OffersSerpItem__description"}).get_text()
            # print(title, '\n')

            address = 'no infromation'
            address = info.find('div', class_='OffersSerpItem__address').get_text()
            # print(address, '\n')

            price = 'no infromation'
            price = info.find('div', class_='Price Price_with-trend Price_interactive OffersSerpItem__price').get_text()
            price = price.replace('сут.', '')  ##
            price = price.replace('/', '')  ##  optional
            price = price.replace('₽', '')  ##
            # print(price, '\n')

            floor = 'no infromation'
            floor = info.find('div', class_='OffersSerpItem__building').get_text()
            # print(floor)

            link = 'no infromation'
            link = info.find('a',
                             class_='Link Link_js_inited Link_size_m Link_theme_islands SerpItemLink OffersSerpItem__link')
            link = link.get('href')
            link = 'https://realty.yandex.ru' + link
            # print(link)

            count_rooms = 'no infromation'
            count_rooms = info.find('a',
                                    class_='Link Link_js_inited Link_size_m Link_theme_islands SerpItemLink OffersSerpItem__link')
            count_rooms = count_rooms.get_text()
            square = count_rooms
            count_rooms = count_rooms.split(',')
            count_rooms = count_rooms[-1]
            count_rooms = count_rooms.replace('-комнатная', '')
            if (len(count_rooms) > 2):
                type_obj = 'студия'
                count_rooms = 1
            else:
                type_obj = 'квартира'
            count_rooms = int(count_rooms)
            # print(count_rooms)

            index = square.find('м²')
            if (index == -1):
                square = 'no information'
            else:
                square = square[:index]
            # print(square)

            metro = 'no infromation'
            metro = info.find('span', class_='MetroStation__title').get_text()
            # print(metro)

            #### ЗАХОДИМ ВНУТРЬ
            response = urlopen(link)
            html_soup = BeautifulSoup(response, 'html.parser')

            publication_date = 'no infromation'
            publication_date = html_soup.find('div', class_='OfferPublishedDate OfferBaseMetaInfo__item').get_text()
            # print(publication_date)

            images = []
            for img in html_soup.findAll('div', class_='GalleryThumbsThumb'):
                # img = img.get('src')
                img = img.find('img', alt='image')
                img = img.get('src')
                img = img[2:-8]
                img = img + 'large'
                # print(img, '\n')
                images.append(img)

            phone = 'no information'
            ####  на один номер уходит примерно 20 секунд на моем ноуте. Периодически происходит что-то странное
            #### (count не печатается, а phone печатается)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome('/Users/slavapirogov/Downloads/chromedriver', options=chrome_options)
            driver.get(link)
            if '<div class="OfferCardContacts__container--1j7yb OfferBaseInfo__contacts">' in driver.page_source:
                button_element = driver.find_element_by_xpath(
                    '/html/body/div[2]/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div[1]/div[4]')
                button_element.click()
                if '<a class="OfferCardContacts__phone--1dmlu"' in driver.page_source:
                    phone = driver.find_element_by_class_name('OfferCardContacts__phone--1dmlu')
                    phone = phone.text
                elif '<div class="OfferCardContacts__phones--3sCEB">' in driver.page_source:
                    phone = driver.find_element_by_class_name('OfferCardContacts__phones--3sCEB')
                    phone = phone.text
            driver.close()

            csv_table = {'title': title, 'address': address, 'price': price, 'count_rooms': count_rooms, 'floor': floor,
                         'type_obj': type_obj, 'square': square, 'publication_date': publication_date, 'link': link,
                         'images': images, 'metro': metro, 'phone': phone}
            writer.writerow(csv_table)


        except AttributeError or IndexError:
            pass
        count += 1
