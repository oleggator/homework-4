from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Component
from pages.photo_page import PhotoPage


class ConfirmModal(Component):
    CONFIRM = '//input[@name="button_delete"]'
    CANCEL = '//a[@data-l="t,cancel"]'

    def confirm(self):
        self.driver.find_element_by_xpath(self.CONFIRM).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()


class LeftActionBar(Component):
    DELETE = '.ic_delete'
    EXPAND = '//span[@data-module="SimplePopup"]'

    def delete(self):
        self.expand()

        WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '.ic_delete'))
        )

        self.driver.find_element_by_css_selector(self.DELETE).click()
        self.confirm()

    def expand(self):
        self.driver.find_element_by_xpath(self.EXPAND).click()

    def confirm(self):
        ConfirmModal(self.driver).confirm()


class MainNavBar(Component):
    PHOTO = '//a[@data-l="aid,NavMenu_AltGroup_Albums"]'

    @property
    def photo_page(self):
        path = self.driver.find_element_by_xpath(self.PHOTO).get_attribute('href')
        return PhotoPage(self.driver, path=path)
