from urllib import parse


class Page:
    BASE_URL = 'https://ok.ru/'

    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.path = kwargs.get('path', '')
        detect_path = kwargs.get('auto_path', False)
        if detect_path:
            self.autodetect_path()

    def autodetect_path(self):
        url = self.driver.current_url
        self.path = parse.urlparse(url).path
        if self.path == 'blank':
            self.path = ''

    def open(self):
        url = parse.urljoin(self.BASE_URL, self.path)
        self.driver.get(url)
        self.driver.maximize_window()


class Component:

    def __init__(self, driver):
        self.driver = driver
