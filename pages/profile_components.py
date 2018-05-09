from pages.my_groups import MyGroupsPage
from pages.page import Component


class LeftNavComponent(Component):
    GROUPS = '//a[@data-l="t,userAltGroup"]'

    def __init__(self, driver):
        super().__init__(driver)

    @property
    def groups(self):
        return self.driver.find_element_by_xpath(self.GROUPS)

    @property
    def groups_page(self):
        path = self.groups.get_attribute('href')

        return MyGroupsPage(self.driver, path=path)
