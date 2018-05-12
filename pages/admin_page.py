from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from pages.page import Page
from pages.settings_components import AddModerForm, PopupUserMenu


class AdminPage(Page):
    BUTTON_ADD_ADMIN = '//*[@id="group-settings-form"]/div[2]/a'
    SELECT_USER = '//*[@id="hook_Block_GroupMembersResultsBlock"]/div/ul/li[2]/div/div[2]/div[1]/a'

    def add_moderator(self):
        self.driver.find_element_by_xpath(self.BUTTON_ADD_ADMIN).click()
        popup_menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.SELECT_USER)))

        ActionChains(self.driver) \
            .move_to_element(popup_menu) \
            .perform()
        self.driver.execute_script(
            "document.getElementsByClassName('gwt-shortcutMenu-content')[0].style.display = 'block';")
        '//*[@id="hook_Block_MainContainer"]/div[5]/table/tbody/tr/td/div/div/div[1]/div/ul[2]/li[4]/a'
        return PopupUserMenu(self.driver)
