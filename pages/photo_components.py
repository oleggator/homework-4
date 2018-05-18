from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.page import Component, url_changer
from pages.waits import web_element_locator


class AlbumType(Enum):
    ALBUM = 0,
    CONTEST = 1


class AlbumCreateModalForm(Component):
    TITLE: str = '//input[@id="field_nameAlbum"]'
    STICKY_ALBUM: str = '//input[@id="field_stickyAlbum_on"]'
    ADMINS_ONLY: str = '//input[@id="field_moderatorsOnlyAlbum_on"]'
    SUBMIT: str = '//input[@id="hook_FormButton_button_save"]'
    CANCEL: str = '//a[@id="button_cancel"]'

    def __init__(self, driver, description: dict) -> None:
        super().__init__(driver)
        self.title: str = description['title']
        self.admins_only: bool = description['admins_only']
        self.sticky_album: bool = description['sticky_album']

    @property
    @web_element_locator((By.XPATH, TITLE))
    def title(self):
        return self.driver.find_element_by_xpath(self.TITLE)

    @title.setter
    def title(self, val: str):
        self.title.send_keys(val)

    @property
    @web_element_locator((By.XPATH, ADMINS_ONLY))
    def admins_only(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.ADMINS_ONLY)

    @admins_only.setter
    def admins_only(self, val: bool):
        elem: WebElement = self.admins_only
        if elem.is_selected() and not val:
            elem.click()
        elif not elem.is_selected and val:
            elem.click()

    @property
    @web_element_locator((By.XPATH, STICKY_ALBUM))
    def sticky_album(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.STICKY_ALBUM)

    @sticky_album.setter
    def sticky_album(self, val: bool):
        elem: WebElement = self.sticky_album
        if elem.is_selected() and not val:
            elem.click()
        elif not elem.is_selected() and val:
            elem.click()

    @url_changer
    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()


class AlbumTypeChoiceModal(Component):
    ALBUM: str = '//i[@class="add-stub_img add-stub_img__album"]/parent::a/parent::div[@class="ugrid_i"]/child::a'
    CONTEST: str = '////i[@class="add-stub_img add-stub_img__contest"]/parent::a/parent::div[@class="ugrid_i"]/child::a'

    @property
    @web_element_locator((By.XPATH, ALBUM))
    def album(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.ALBUM)

    @property
    @web_element_locator((By.XPATH, CONTEST))
    def contest(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.CONTEST)

    def choose(self, album_type: AlbumType):
        if album_type == AlbumType.ALBUM:
            self.album.click()
        elif album_type == AlbumType.CONTEST:
            self.contest.click()


class AlbumCreateButton(Component):
    ALBUM_CREATE: str = '.ic_photos'

    def create_album(self, album_type: AlbumType, description: dict):
        self.driver.find_element_by_css_selector(self.ALBUM_CREATE).click()
        AlbumTypeChoiceModal(self.driver).choose(album_type)
        AlbumCreateModalForm(self.driver, description).submit()
