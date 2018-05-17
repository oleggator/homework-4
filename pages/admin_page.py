from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Page
from pages.settings_components import PopupUserMenu


class AdminPage(Page):
    BUTTON_ADD_ADMIN = '//*[@id="group-settings-form"]/div[2]/a'
    ADMINISTRATION_LIST_PAGE = '//*[@id="GroupMembersMenu"]/div/div/a[2]'
    ADMINISTRATION_LIST = '//*[@id="hook_Block_GroupMembersResultsBlock"]/div/ul'

    def add_moderator(self, name):
        self.driver.find_element_by_xpath(self.BUTTON_ADD_ADMIN).click()

        popup_menu = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, name)))

        ActionChains(self.driver) \
            .move_to_element(popup_menu) \
            .perform()
        self.driver.execute_script(
            "document.getElementsByClassName('gwt-shortcutMenu-content')[0].style.display = 'block';")
        PopupUserMenu(self.driver).assign_as_moderator.add_grant()
        return self

    def to_administration_list(self):
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, self.ADMINISTRATION_LIST_PAGE))).click()
        self.driver.find_element_by_xpath(self.ADMINISTRATION_LIST_PAGE).click()

    def remove_moderator(self, name):
        # popup_menu = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.LINK_TEXT, name)))

        popup_menu = self.driver.find_element_by_link_text(name)

        ActionChains(self.driver) \
            .move_to_element(popup_menu) \
            .perform()

        self.driver.execute_script(
            "document.getElementsByClassName('gwt-shortcutMenu-content')[0].style.display = 'block';")
        return PopupUserMenu(self.driver)

    def is_exists_moder_href(self, name):
        try:
            self.driver.find_elements_by_link_text(name)
        except Exception:
            return False
        return True
