from pages.page import Component, url_changer
from pages.photo_page import PhotoPage


class ConfirmModal(Component):
    CONFIRM = '//input[@name="button_delete"]'
    CANCEL = '//a[@data-l="t,cancel"]'

    def confirm(self):
        self.driver.find_element_by_xpath(self.CONFIRM).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()


class LeftActionBar(Component):
    DELETE = 'ic_delete'

    @url_changer
    def delete(self):
        self.driver.execute_script('''
            document.getElementsByClassName('{}')[0].click()
        '''.format(self.DELETE))
        ConfirmModal(self.driver).confirm()


class MainNavBar(Component):
    PHOTO = '//a[@data-l="aid,NavMenu_AltGroup_Albums"]'

    @property
    def photo_page(self):
        path = self.driver.find_element_by_xpath(self.PHOTO).get_attribute('href')
        return PhotoPage(self.driver, path=path)
