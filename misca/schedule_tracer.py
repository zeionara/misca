from datetime import datetime, timedelta
import urllib.request
from bs4 import BeautifulSoup

from .MovieSession import MovieSession, DATE_PATTERN
from .MovieTheater import MovieTheater


def trace_schedule(max_price: float = None, movie: str = None, theater: int = None, ndays: int = 0):
    assert ndays < 5, 'Cannot look 5 or more days ahead'

    now = datetime.now()

    dates = [now]

    for i in range(1, ndays + 1):
        dates.append(now + timedelta(days = i))

    dates_as_string = [date.strftime(DATE_PATTERN) for date in dates]

    sessions = []

    for date_as_string in dates_as_string:
        url = f'https://www.mirage.ru/spb/schedule/{date_as_string}/'

        response = urllib.request.urlopen(url)
        html_content = response.read().decode('utf-8')
        parsed_page = BeautifulSoup(html_content, 'html.parser')

        sessions_container = parsed_page.find_all('div', {'class': 'session-box'})[0]

        current_movie_theater = None

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
