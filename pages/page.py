from functools import wraps
from typing import Tuple, Callable, Any
from urllib import parse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

Locator = Tuple[By, str]
LocatorAccessor = Callable[[Any], Locator]


class Page:
    BASE_URL: str = 'https://ok.ru/'

    def __init__(self, driver, **kwargs) -> None:
        self.driver = driver
        self.path: str = kwargs.get('path', '')

    def open(self) -> 'Page':
        url: str = self.url
        self.driver.get(url)
        self.driver.maximize_window()
        return self

    @property
    def url(self):
        return parse.urljoin(self.BASE_URL, self.path)


class Component:

    def __init__(self, driver) -> None:
        self.driver = driver


def url_changer(f):
    @wraps(f)
    def wrapped(self, *f_args, **f_kwargs):
        current_url: str = self.driver.current_url
        f(self, *f_args, **f_kwargs)
        WebDriverWait(self.driver, 10).until_not(expected_conditions.url_to_be(current_url))

    return wrapped
