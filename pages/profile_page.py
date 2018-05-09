from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from pages.my_groups import MyGroupsPage
from pages.page import Page
from pages.profile_components import LeftNavComponent


class ProfilePage(Page):

    def __init__(self, driver):
        super().__init__(driver)
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.XPATH, '//div[@data-l="t,navigation"]'))
        )

    @property
    def left_nav(self):
        return LeftNavComponent(self.driver)

    def get_groups_page(self):
        groups = self.left_nav.groups
        groups_path = groups.get_attribute("href")
        groups.click()
        return MyGroupsPage(self.driver, groups_path)
