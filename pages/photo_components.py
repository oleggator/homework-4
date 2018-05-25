import os
from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

from pages.page import Component, url_changer
from pages.waits import web_element_locator, button_locator


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


class ContestCreateModalForm(Component):
    TITLE: str = '//input[@id="field_name"]'
    DESCRIPTION: str = '//textarea[@id="field_descr"]'
    TILL_DATE: str = '//input[@id="field_till"]'
    STICKY_ALBUM: str = '//input[@id="field_stickyWhenCompleted_on"]'
    ADMINS_ONLY: str = '//input[@id="field_moderatorsOnly_on"]'
    COVER: str = 'img.add-happening_poster_img'
    COVER_UPLOAD: str = '//input[@name="photo"]'
    SUBMIT: str = '//input[@id="hook_FormButton_button_create_comp"]'
    CANCEL: str = '//a[@id="button_cancel"]'

    def __init__(self, driver, description: dict) -> None:
        super().__init__(driver)
        self.title: str = description['title']
        self.description = description['description']
        self.till_date = description['till_date']
        self.cover = description['cover']
        self.admins_only: bool = description['admins_only']
        self.sticky_album: bool = description['sticky_album']

    @property
    def title(self):
        return self.driver.find_element_by_xpath(self.TITLE)

    @title.setter
    def title(self, val: str):
        self.title.send_keys(val)

    @property
    def description(self):
        return self.driver.find_element_by_xpath(self.DESCRIPTION)

    @description.setter
    def description(self, val: str):
        self.description.send_keys(val)

    @property
    def till_date(self):
        return self.driver.find_element_by_xpath(self.TILL_DATE)

    @till_date.setter
    def till_date(self, val: str):
        self.till_date.send_keys(val)
        self.till_date.send_keys(Keys.RETURN)

    @property
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
    def cover_upload(self):
        return self.driver.find_element_by_xpath(self.COVER)

    @cover_upload.setter
    def cover_upload(self, val: str):
        path = os.path.abspath(val)
        self.driver.find_element_by_xpath(self.COVER).send_keys(path)

    @property
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
    CONTEST: str = '//i[@class="add-stub_img add-stub_img__contest"]/parent::a/parent::div[@class="ugrid_i"]/child::a'

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
    ALBUM_CREATE: str = '.portlet_h_ac.lp.__shift'

    @property
    @button_locator((By.CSS_SELECTOR, ALBUM_CREATE))
    def album_create_button(self):
        return self.driver.find_element_by_css_selector(self.ALBUM_CREATE)

    def create_album(self, album_type: AlbumType, description: dict):
        self.album_create_button.send_keys(Keys.ENTER)
        AlbumTypeChoiceModal(self.driver).choose(album_type)

        if album_type == AlbumType.ALBUM:
            AlbumCreateModalForm(self.driver, description).submit()
        elif album_type == AlbumType.CONTEST:
            ContestCreateModalForm(self.driver, description).submit()
