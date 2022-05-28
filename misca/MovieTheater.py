import re

THEATER_ID_PATTERN = re.compile('/.*/cinema/([0-9]+)/')

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
