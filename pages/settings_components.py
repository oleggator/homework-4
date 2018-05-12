from pages.page import Component


class AddModerForm(Component):
    RADIO_BUTTON_MODERATOR = '//*[@id="field_index_0"]'
    ADD_BUTTON = '//*[@id="hook_FormButton_button_grant"]'

    def add_grant(self):
        self.driver.find_element_by_xpath(self.RADIO_BUTTON_MODERATOR).click()
        self.driver.find_element_by_xpath(self.ADD_BUTTON).click()


class PopupUserMenu(Component):
    ASSIGN_MODERATOR_POPUP_ITEM = '//*[@id="hook_Block_MainContainer"]/div[5]/table/tbody/tr/td/div/div/div[1]/div/ul[2]/li[2]/a'
    REMOVE_MODERATOR_POPUP_ITEM = '//*[@id="hook_Block_MainContainer"]/div[5]/table/tbody/tr/td/div/div/div[1]/div/ul[2]/li[4]/a'

    @property
    def assign_as_moderator(self) -> AddModerForm:
        self.driver.find_element_by_xpath(self.ASSIGN_MODERATOR_POPUP_ITEM).click()
        return AddModerForm(self.driver)

    def remove_as_moderator(self):
        self.driver.find_element_by_xpath(self.REMOVE_MODERATOR_POPUP_ITEM).click()
