from pages.group_components import LeftActionBar, MainNavBar
from pages.page import Page
from pages.photo_page import PhotoPage
from pages.settings_page import SettingsPage


class GroupPage(Page):
    JOIN_BUTTON = '//*[@id="hook_Block_LeftColumnTopCardAltGroup"]/ul/div[2]/a'
    DROPDOWN_BUTTON = '//*[@id="hook_Block_LeftColumnTopCardAltGroup"]/ul/div[2]/div[1]/span'
    UNJOIN_BUTTON_CLASS = 'dropdown_cnt'
    NAME_TEXT = '//*[@id="hook_Block_MiddleColumnTopCardAltGroup"]/div[2]/div/div[1]/div/span/h1'
    DESCRIPTION_TEXT = '//*[@id="hook_Block_MiddleColumnTopCardAltGroup"]/div[2]/div/div[2]/div[1]/div[2]'
    CATEGORY_TEXT = '//*[@id="hook_Block_MiddleColumnTopCardAltGroup"]/div[2]/div/div[2]/div[1]/div[1]'

    @property
    def left_action_bar(self) -> LeftActionBar:
        return LeftActionBar(self.driver)

    @property
    def main_nav_bar(self) -> MainNavBar:
        return MainNavBar(self.driver)

    def to_photo_page(self) -> PhotoPage:
        photo_page = self.main_nav_bar.photo_page
        photo_page.open()
        return photo_page

    def to_settings_page(self) -> SettingsPage:
        setting_page = self.left_action_bar.to_settings_page
        return setting_page

    def delete_group(self):
        self.open()
        self.left_action_bar.delete()

    def join(self):
        self.driver.find_element_by_xpath(self.JOIN_BUTTON).click()
        return self

    def get_name(self):
        return self.driver.find_element_by_xpath(self.NAME_TEXT).text

    def get_description(self):
        return self.driver.find_element_by_xpath(self.DESCRIPTION_TEXT).text

    def get_category(self):
        return self.driver.find_element_by_xpath(self.CATEGORY_TEXT).text

    def get_type(self):
        return self.driver.find_element_by_xpath(self.TYPE_TEXT).text

    def unjoin(self):
        # self.driver.execute_script(
        #     "document.getElementsByClassName('{}')[0].style.display = 'block';".format(self.UNJOIN_BUTTON_CLASS))
        # self.driver.find_elements_by_class_name(self.UNJOIN_BUTTON_CLASS).click()
        self.driver.find_element_by_xpath(self.DROPDOWN_BUTTON).click()
        unjoin_button = self.driver.find_element_by_class_name(self.UNJOIN_BUTTON_CLASS)
        unjoin_button.click()
        return self
