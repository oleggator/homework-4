from urllib import parse


class Page:
    BASE_URL = 'https://ok.ru/'

    def __init__(self, driver, path=''):
        self.driver = driver
        self.path = path

    def open(self):
        url = parse.urljoin(self.BASE_URL, self.path)
        self.driver.get(url)
        self.driver.maximize_window()


class Component:

    def __init__(self, driver):
        self.driver = driver


