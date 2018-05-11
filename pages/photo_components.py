from enum import Enum

from pages.page import Component


class AlbumType(Enum):
    ALBUM = 0,
    CONTEST = 1


class AlbumCreateModalForm(Component):
    TITLE = '//input[@id="field_nameAlbum"]'
    STICKY_ALBUM = '//input[@id="field_stickyAlbum_on"]'
    ADMINS_ONLY = '//input[@id="field_moderatorsOnlyAlbum_on"]'
    SUBMIT = '//input[@id="hook_FormButton_button_save"]'
    CANCEL = '//a[@id="button_cancel"]'

    def __init__(self, driver, description):
        super().__init__(driver)
        self.title = description['title']
        self.admins_only = description['admins_only']
        self.sticky_album = description['sticky_album']

    @property
    def title(self):
        return self.driver.find_element_by_xpath(self.TITLE)

    @title.setter
    def title(self, val):
        self.title.send_keys(val)

    @property
    def admins_only(self):
        return self.driver.find_element_by_xpath(self.ADMINS_ONLY)

    @admins_only.setter
    def admins_only(self, val):
        elem = self.admins_only
        if elem.is_selected() and not val:
            elem.click()
        elif not elem.is_selected and val:
            elem.click()

    @property
    def sticky_album(self):
        return self.driver.find_element_by_xpath(self.STICKY_ALBUM)

    @sticky_album.setter
    def sticky_album(self, val):
        elem = self.sticky_album
        if elem.is_selected() and not val:
            elem.click()
        elif not elem.is_selected() and val:
            elem.click()

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()


class AlbumTypeChoiceModal(Component):
    ALBUM = '//i[@class="add-stub_img add-stub_img__album"]/parent::a/parent::div[@class="ugrid_i"]/child::a'
    CONTEST = '////i[@class="add-stub_img add-stub_img__contest"]/parent::a/parent::div[@class="ugrid_i"]/child::a'

    @property
    def album(self):
        return self.driver.find_element_by_xpath(self.ALBUM)

    @property
    def contest(self):
        return self.driver.find_element_by_xpath(self.CONTEST)

    def choose(self, album_type):

        if album_type == AlbumType.ALBUM:
            self.album.click()
        elif album_type == AlbumType.CONTEST:
            self.contest.click()


class AlbumCreateButton(Component):
    ALBUM_CREATE = '.ic_photos'

    def create_album(self, album_type, description):
        self.driver.find_element_by_css_selector(self.ALBUM_CREATE).click()
        AlbumTypeChoiceModal(self.driver).choose(album_type)
        AlbumCreateModalForm(self.driver, description).submit()
