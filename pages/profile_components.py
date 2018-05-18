from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from pages.my_groups import MyGroupsPage
from pages.page import Component
from pages.waits import web_element_locator


class LeftNavComponent(Component):
    GROUPS: str = '//a[@data-l="t,userAltGroup"]'

    def __init__(self, driver) -> None:
        super().__init__(driver)

    @property
    @web_element_locator((By.XPATH, GROUPS))
    def groups(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.GROUPS)

    @property
    def groups_page(self) -> MyGroupsPage:
        path: str = self.groups.get_attribute('href')
        return MyGroupsPage(self.driver, path=path)
