from urllib import parse


class Page:
    BASE_URL = 'https://ok.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = parse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class Component:

    def __init__(self, driver):
        self.driver = driver
