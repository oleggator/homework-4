from pages.page import Component


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
        self.driver.find_element_by_css_selector(self.DELETE).click()
        self.confirm()

    def expand(self):
        self.driver.find_element_by_xpath(self.EXPAND).click()

    def confirm(self):
        ConfirmModal(self.driver).confirm()
