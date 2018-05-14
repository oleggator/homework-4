from pages.admin_page import AdminPage
from pages.application_page import ApplicationPage
from pages.general_page import GeneralPage
from pages.managment_page import ManagmentPage
from pages.page import Page
from pages.settings_components import AddGroupLinksPopup


class SettingsPage(Page):
    GENERAL_ITEM = '//*[@id="RightColumnAltGroupSettingsCatalog"]/div/div/a[1]'
    MANAGEMENT_ITEM = '//*[@id="RightColumnAltGroupSettingsCatalog"]/div/div/a[2]'
    ADMIN_ITEM = '//*[@id="RightColumnAltGroupSettingsCatalog"]/div/div/a[3]'
    APPLICATION_ITEM = '//*[@id="RightColumnAltGroupSettingsCatalog"]/div/div/a[4]'
    GROUP_LINKS_ITEM = '//*[@id="altGroupsOfFriendsPanel"]/div[2]/div/a'

    def to_admin_page(self) -> AdminPage:
        path = self.driver.find_element_by_xpath(self.ADMIN_ITEM).get_attribute('href')
        admin_page = AdminPage(self.driver, path=path)
        admin_page.open()
        return AdminPage(self.driver, path=path)

    def to_management_page(self) -> ManagmentPage:
        path = self.driver.find_element_by_xpath(self.MANAGEMENT_ITEM).get_attribute('href')
        return ManagmentPage(self.driver, path=path)

    def to_general_page(self) -> GeneralPage:
        path = self.driver.find_element_by_xpath(self.GENERAL_ITEM).get_attribute('href')
        return GeneralPage(self.driver, path=path)

    def to_application_page(self) -> ApplicationPage:
        path = self.driver.find_element_by_xpath(self.APPLICATION_ITEM).get_attribute('href')
        return ApplicationPage(self.driver, path=path)

    def add_group_links(self):
        self.driver.find_element_by_xpath(self.GROUP_LINKS_ITEM).click()
        return AddGroupLinksPopup(self.driver)
