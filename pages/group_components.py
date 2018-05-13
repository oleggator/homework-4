from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Component, url_changer
from pages.photo_page import PhotoPage
from pages.settings_page import SettingsPage


class ConfirmModal(Component):
    CONFIRM = '//input[@name="button_delete"]'
    CANCEL = '//a[@data-l="t,cancel"]'

    def confirm(self):
        self.driver.find_element_by_xpath(self.CONFIRM).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()


class LeftActionBar(Component):
    DELETE = 'ic_delete'
    SETTINGS: str = '//*[@id="hook_Block_LeftColumnTopCardAltGroup"]/ul/li[4]/a'

    @url_changer
    def delete(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.{}'.format(self.DELETE)))
        )
        self.driver.execute_script('''
            document.getElementsByClassName('{}')[0].click()
        '''.format(self.DELETE))
        ConfirmModal(self.driver).confirm()

    @property
    def to_settings_page(self) -> SettingsPage:
        path = self.driver.find_element_by_xpath(self.SETTINGS).get_attribute('href')
        setting_page = SettingsPage(self.driver, path=path)
        setting_page.open()
        return setting_page


class MainNavBar(Component):
    PHOTO = '//a[@data-l="aid,NavMenu_AltGroup_Albums"]'

    @property
    def photo_page(self) -> PhotoPage:
        path = self.driver.find_element_by_xpath(self.PHOTO).get_attribute('href')
        return PhotoPage(self.driver, path=path)
