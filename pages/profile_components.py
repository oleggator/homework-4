from pages.page import Component


class LeftNavComponent(Component):
    GROUPS = '//a[@data-l="t,userAltGroup"]'

    def __init__(self, driver):
        super().__init__(driver)

    @property
    def groups(self):
        return self.driver.find_element_by_xpath(self.GROUPS)
