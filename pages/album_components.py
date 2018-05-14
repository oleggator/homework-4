from typing import List
from urllib import parse

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Component


class AlbumDeleteConfirmModal(Component):
    CONFIRM: str = '//input[@id="hook_FormButton_button_remove_confirm"]'
    CANCEL: str = '//input[@id="button_cancel_confirm"]'

    def confirm(self) -> None:
        self.driver.find_element_by_xpath(self.CONFIRM).click()

    def cancel(self) -> None:
        self.driver.find_element_by_xpath(self.CANCEL).click()


class AlbumControlPanel(Component):
    DELETE: str = 'ul.controls-list > li:nth-child(2) > a'
    EDIT: str = '.ic12_edit'
    TITLE: str = 'span.photo-h_cnt_t'

    def delete_album(self) -> None:
        self.edit_button.click()
        self.delete_button.click()
        AlbumDeleteConfirmModal(self.driver).confirm()

    @property
    def delete_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DELETE)

    @property
    def edit_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.EDIT)

    @property
    def title(self) -> str:
        return self.driver.find_element_by_css_selector(self.TITLE).text


class ImageCard(Component):
    EDIT_TEMPLATE: str = '//div[@id="trigger_{}"]'
    DELETE_TEMPLATE: str = '#popup_{} .ic_delete'
    MAKE_MAIN_TEMPLATE: str = '#popup_{} .ic_make-main'
    EDIT_DESCRIPTION_TEMPLATE: str = '//[@id=descrInp{}]'

    def __init__(self, driver, src):
        super().__init__(driver)
        self.src = src
        query_string: str = parse.urlparse(self.src).query
        self.id: str = parse.parse_qs(query_string)['id'][0]
        self.EDIT_DESCRIPTION: str = self.EDIT_DESCRIPTION_TEMPLATE.format(self.id)
        self.EDIT: str = self.EDIT_TEMPLATE.format(self.id)
        self.DELETE: str = self.DELETE_TEMPLATE.format(self.id)
        self.MAKE_MAIN: str = self.MAKE_MAIN_TEMPLATE.format(self.id)

    @property
    def description(self) -> str:
        return self.driver.find_element_by_xpath(self.EDIT_DESCRIPTION).value()

    @property
    def edit(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.EDIT)

    @property
    def delete_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DELETE)

    @description.setter
    def description(self, value) -> None:
        self.driver.find_element_by_xpath(self.EDIT_DESCRIPTION).send_keys(value)

    def make_main(self):
        pass

    def delete_image_card(self) -> None:
        self.driver.execute_script('''
            document.querySelector('{}').click()
        '''.format(self.DELETE))


class PhotosPanel(Component):
    LOADER: str = '//div[@class="photo-card_loading"]'
    PHOTOS: str = 'span.photo-card_cnt img'

    def get_last(self):
        imgs: List[WebElement] = self.driver.find_elements_by_css_selector(self.PHOTOS)
        src: str = imgs[0].get_attribute('src')
        return ImageCard(self.driver, src)

    def wait_uploading(self) -> None:
        WebDriverWait(self.driver, 60).until_not(
            expected_conditions.presence_of_element_located((By.XPATH, self.LOADER))
        )


class AlbumUploadPhotoButton(Component):
    UPLOAD: str = '//input[@name="photo"]'

    def upload(self, path) -> ImageCard:
        self.driver.find_element_by_xpath(self.UPLOAD).send_keys(path)
        photos_panel: PhotosPanel = PhotosPanel(self.driver)
        photos_panel.wait_uploading()
        return photos_panel.get_last()
