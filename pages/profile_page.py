from pages.my_groups import MyGroupsPage
from pages.page import Page
from pages.profile_components import LeftNavComponent


class ProfilePage(Page):
    NAME = '//*[@id="hook_Block_Navigation"]/div/div/a[1]/span'

    def __init__(self, driver):
        super(ProfilePage, self).__init__(driver)
        self.name = self.driver.find_element_by_xpath(self.NAME).text

    @property
    def left_nav(self):
        return LeftNavComponent(self.driver)

    def to_groups_page(self) -> MyGroupsPage:
        my_groups_page: MyGroupsPage = self.left_nav.groups_page
        my_groups_page.open()
        return my_groups_page

    def get_name(self):
        return self.driver.find_element_by_xpath(self.NAME).text()
