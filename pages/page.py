from functools import wraps
from urllib import parse

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Page:
    BASE_URL = 'https://ok.ru/'

    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.path = kwargs.get('path', '')

    def open(self):
        url = self.url
        self.driver.get(url)
        self.driver.maximize_window()

    @property
    def url(self):
        return parse.urljoin(self.BASE_URL, self.path)


class Component:

    def __init__(self, driver):
        self.driver = driver


def url_changer(f):
    @wraps(f)
    def wrapped(self, *f_args, **f_kwargs):
        current_url = self.driver.current_url
        f(self, *f_args, **f_kwargs)
        WebDriverWait(self.driver, 10).until_not(expected_conditions.url_to_be(current_url))

    return wrapped
