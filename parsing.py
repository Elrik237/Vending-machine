import requests
from bs4 import BeautifulSoup
from storage_service import StorageService
from model_snacks import ListOfSnacks


class Parser:
    def __init__(self):
        self.storage_service = StorageService()

        self.URL = 'https://kdvonline.ru/catalog/vafli-11'
        self.HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4400.8 Safari/537.36',
            'accept': '*/*'
        }

    def get_html(self, url, params=None):
        r = requests.get(url, headers=self.HEADERS, params=params)
        return r

    def get_content(self, html):
        session = self.storage_service.create_session()
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.find_all('div', class_="c3s8K6a5X")
        quantity = 50

        for item in items:
            title = item.find('a', class_='fKV5--oM0').get_text().replace('\xa0г', '') + 'г',
            price = item.find('div', class_='a2iP1cx1b').get_text(),


            list_of_snacks = ListOfSnacks(title[0], price[0], quantity)
            session.add(list_of_snacks)
            session.commit()
            session.close()

    def parse(self):
        html = self.get_html(self.URL)
        if html.status_code == 200:
            self.get_content(html.text)

        else:
            print('Error, status_code not 200')
