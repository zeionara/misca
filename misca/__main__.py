import math
import re
from datetime import datetime
import click
import urllib.request
from bs4 import BeautifulSoup


@click.group()
def main():
    pass


DATE_TIME_PATTERN = '%d.%m.%Y.%H:%M'
THEATER_ID_PATTERN = re.compile('/spb/cinema/([0-9]+)/')


class MovieSession:
    def __init__(self, html_content: BeautifulSoup, date, theater):
        self.title = html_content.find_next('div', {'class': 'title'}).getText()

        self.__date_as_string = date
        time = html_content.find_next('div', {'class': 'time'}).get_text()
        self.__time_as_string = time

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
        return f'{self.title:<50} 🌎 {str(self.theater):<50} @ {self.room:<20} 📅 {self.__date_as_string} 🕑 {self.__time_as_string} 💰 {", ".join(map(str, self.prices))}'

    def __repr__(self):
        return self.__str__()


class MovieTheater:
    def __init__(self, html_content):
        self.title = html_content.get_text().strip()  # .capitalize()

        link = html_content.a['href']
        match_ = THEATER_ID_PATTERN.fullmatch(link)

        self.id = int(match_.group(1))

    def setup_address(self, html_content):
        self.address = html_content.get_text().strip()

    def __str__(self):
        return f'{self.title} [{self.id}] 🗺️ {self.address}'

    def __repr__(self):
        return self.__str__()


@main.command()
@click.option('--max-price', '-xp', type = int, default = None)
@click.option('--movie', '-m', type = str, default = None)
@click.option('--theater', '-t', type = int, default = None)
def print_hello_world(max_price: int, movie: str, theater: int):
    date_as_string = '29.05.2022'

    url = f'https://www.mirage.ru/spb/schedule/{date_as_string}/'

    response = urllib.request.urlopen(url)
    html_content = response.read().decode('utf-8')
    parsed_page = BeautifulSoup(html_content, 'html.parser')

    # print(len(parsed_page.find_all('div', {'class': 'session'})))

    # sessions = [MovieSession(session, date_as_string) for session in parsed_page.find_all('div', {'class': 'session'})]

    sessions_container = parsed_page.find_all('div', {'class': 'session-box'})[0]

    current_movie_theater = None

    sessions = []

    for element in sessions_container.find_all('div', recursive = False):
        element_class = element['class'][0]
        if element_class == 'md-title':
            current_movie_theater = MovieTheater(element)
        elif element_class == 'adds':
            current_movie_theater.setup_address(element)
        elif element_class == 'session-slider':
            sessions.extend(MovieSession(session, date_as_string, current_movie_theater) for session in element.find_all('div', {'class': 'session'}))

    for session in sessions:
        if (
            max_price is None or session.max_price <= max_price
        ) and (
            movie is None or session.title == movie
        ) and (
            theater is None or session.theater.id == theater
        ):
            print(session)

    # print(MovieSession(sessions[0], date_as_string))
    # print(len(sessions))


if __name__ == '__main__':
    main()
