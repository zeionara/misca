from datetime import datetime
import math
from bs4 import BeautifulSoup

from .MovieTheater import MovieTheater

DATE_PATTERN = '%d.%m.%Y'
DATE_TIME_PATTERN = f'{DATE_PATTERN}.%H:%M'


class MovieSession:
    def __init__(self, html_content: BeautifulSoup, date: str, theater: MovieTheater):
        self.title = html_content.find_next('div', {'class': 'title'}).getText()

        self._date_as_string = date
        time = html_content.find_next('div', {'class': 'time'}).get_text()
        self._time_as_string = time

        date_and_time = f'{date}.{time}'

        self.time = datetime.strptime(date_and_time, DATE_TIME_PATTERN)

        labels = [item.get_text() for item in html_content.find_next('div', {'class': 'labels'}).find_all('span', recursive = False)]

        self.room = labels[0] if len(labels) > 0 else None

        prices = [int(item.get_text().strip()[:-1]) for item in html_content.find_next('div', {'class': 'place-price'}).find_all('div', recursive = False)]

        self.min_price = min(prices)
        self.max_price = max(prices)

        self.mean_price = math.ceil(sum(prices) / len(prices))

        self.prices = prices

        self.theater = theater

    def __str__(self):
        # return f'{self.title} @ {self.room} 📅 {self.__date_as_string} 🕑 {self.__time_as_string} 💰 {self.mean_price}'
        return f'{self.title:<50} 🌎 {str(self.theater):<50} @ {self.room:<20} 📅 {self._date_as_string} {"(" + self.time.strftime("%A") + ")":<15} 🕑 {self._time_as_string} 💰 {", ".join(map(str, self.prices))}'

    def __repr__(self):
        return self.__str__()
