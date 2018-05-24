from typing import Callable

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions

from pages import waits
from pages.page import Component
from pages.waits import web_element_locator, dynamic_web_element_locator, button_locator


class ConfirmMakeMainModal(Component):
    CONFIRM = '#hook_FormButton_button_cover_confirm'
    CANCEL = '#hook_Form_PopLayerSetAltGroupAlbumCoverForm a'

    def __init__(self, driver, on_confirm: Callable = None, on_cancel: Callable = None):
        super().__init__(driver)
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

    def confirm(self):
        self.confirm_button.click()
        if self.on_confirm is not None:
            self.on_confirm()

    def cancel(self):
        self.cancel_button.click()
        if self.on_cancel is not None:
            self.on_cancel()

    @property
    @button_locator((By.CSS_SELECTOR, CANCEL))
    def cancel_button(self):
        return self.driver.find_element_by_css_selector(self.CANCEL)

    @property
    @button_locator((By.CSS_SELECTOR, CONFIRM))
    def confirm_button(self):
        return self.driver.find_element_by_css_selector(self.CONFIRM)


class ExpandedImageCard(Component):
    DESCRIPTION = 'span[data-link-source="photo-desc"]'

    @property
    @web_element_locator((By.CSS_SELECTOR, DESCRIPTION))
    def description(self) -> str:
        return self.driver.find_element_by_css_selector(self.DESCRIPTION).text


class ImageCard(Component):
    EDIT_TEMPLATE: str = '//div[@id="trigger_{}"]'
    DELETE_BUTTON_TEMPLATE: str = '#popup_{} .ic_delete'
    MAKE_MAIN_TEMPLATE: str = '#popup_{} .ic_make-main'
    EDIT_DESCRIPTION_TEMPLATE: str = '//textarea[@id="descrInp{}"]'
    IMAGE_TEMPLATE: str = '#img_{}'
    RESTORE_BUTTON_TEMPLATE: str = '#hook_Block_DeleteRestorePhotoMRB{} .photo-sc_i_utility_undo-delete'
    CHECK_BUTTON_TEMPLATE: str = '#hook_Block_PhotoCardV2Block{} .selectable-card_ic'

    def __init__(self, driver, img_id: str):
        super().__init__(driver)
        self.id: str = img_id
        self.IMAGE = self.IMAGE_TEMPLATE.format(self.id)
        self.EDIT_DESCRIPTION: str = self.EDIT_DESCRIPTION_TEMPLATE.format(self.id)
        self.EDIT: str = self.EDIT_TEMPLATE.format(self.id)
        self.DELETE: str = self.DELETE_BUTTON_TEMPLATE.format(self.id)
        self.MAKE_MAIN: str = self.MAKE_MAIN_TEMPLATE.format(self.id)
        self.RESTORE: str = self.RESTORE_BUTTON_TEMPLATE.format(self.id)
        self.CHECK_BUTTON: str = self.CHECK_BUTTON_TEMPLATE.format(self.id)

    @property
    def description(self) -> str:
        return self.driver.find_element_by_xpath(self.EDIT_DESCRIPTION).get_attribute('value')

    @property
    def edit(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.EDIT)

    @property
    def delete_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DELETE)

    @description.setter
    def description(self, value) -> None:
        self.driver.find_element_by_xpath(self.EDIT_DESCRIPTION).send_keys(value)

    @property
    def image_src(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.IMAGE)

    @property
    def check_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.CHECK_BUTTON)

    @property
    @dynamic_web_element_locator(lambda self: (By.CSS_SELECTOR, self.RESTORE))
    def restore_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.RESTORE)

    def restore(self) -> None:
        restore_button = self.restore_button
        if restore_button is None:
            return
        restore_button.click()

    def check(self):
        self.check_button.click()

    @dynamic_web_element_locator(lambda self: (By.CSS_SELECTOR, self.MAKE_MAIN))
    def make_main(self):
        self.driver.execute_script('''
            document.querySelector(`{}`).click()
        '''.format(self.MAKE_MAIN))

        return ConfirmMakeMainModal(self.driver)

    def delete_image_card(self) -> None:
        self.driver.execute_script('''
            document.querySelector(`{}`).click()
        '''.format(self.DELETE))
        waits.wait(self.driver).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.RESTORE))
        )

    def expand(self) -> ExpandedImageCard:
        self.image_src.click()
        return ExpandedImageCard(self.driver)
