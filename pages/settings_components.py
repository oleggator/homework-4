from enum import Enum

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Component


class ModerForm(Component):
    RADIO_BUTTON_MODERATOR = '//*[@id="field_index_0"]'
    ADD_BUTTON = '//*[@id="hook_FormButton_button_grant"]'
    REMOVE_BUTTON = '//*[@id="hook_FormButton_button_revoke_confirm"]'
    POPUP_DIALOG = '//*[@id="popLayer_mo"]'

    def add_grant(self):
        self.driver.find_element_by_xpath(self.RADIO_BUTTON_MODERATOR).click()
        self.driver.find_element_by_xpath(self.ADD_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, self.POPUP_DIALOG)))

    def remove_grant(self):
        self.driver.find_element_by_xpath(self.REMOVE_BUTTON).click()


class GeneralForm(Component):
    NAME_GROUP_INPUT = '//*[@id="field_name"]'
    DESCRIPTION_GROUP_INPUT = '//*[@id="field_description"]'
    CATEGORY = '//*[@id="field_pageSuperCategory"]'
    SUBCATEGORY = '//*[@id="field_pageMixedCategory"]'
    CATEGORY_AFTER_SAVE = '//*[@id="categoriesCollapsedId"]/div[2]/span[1]'
    SAVE_BUTTON = '//*[@id="hook_FormButton_button_save_settings"]'
    TIP = '//*[@id="hook_Block_TipBlock"]/div/div'
    TYPE_TEXT = '//*[@id="group-settings-form"]/div/div[1]/div[2]/div/span[1]'

    class Categories(Enum):
        BRAND = 'BRAND'
        LOCAL = 'LOCAL'
        STAR = 'STAR'
        PUBLIC = 'PUBLIC'

    def __init__(self, driver):
        super().__init__(driver)

    @property
    def name(self):
        return self.driver.find_element_by_xpath(self.NAME_GROUP_INPUT)

    @name.setter
    def name(self, val):
        input = self.driver.find_element_by_xpath(self.NAME_GROUP_INPUT)
        input.clear()
        input.send_keys(val)

    @property
    def description(self):
        return self.driver.find_element_by_xpath(self.DESCRIPTION_GROUP_INPUT)

    @description.setter
    def description(self, val):
        input = self.driver.find_element_by_xpath(self.DESCRIPTION_GROUP_INPUT)
        input.clear()
        input.send_keys(val)

    @property
    def category(self):
        return self.driver.find_element_by_xpath(self.CATEGORY_AFTER_SAVE).text

    @category.setter
    def category(self, category: str):
        select_category = Select(self.driver.find_element_by_xpath(self.CATEGORY))
        select_category.select_by_value(category)

    @property
    def subcategory(self):
        select_subcategory = Select(self.driver.find_element_by_xpath(self.SUBCATEGORY))
        return select_subcategory.first_selected_option.text

    @subcategory.setter
    def subcategory(self, subcategory: str):
        select_category = Select(self.driver.find_element_by_xpath(self.SUBCATEGORY))
        if subcategory not in [o.get_attribute('value') for o in select_category.options]:
            select_category.select_by_index(0)
        else:
            select_category.deselect_by_value(subcategory)

    @property
    def type(self):
        return self.driver.find_element_by_xpath(self.TYPE_TEXT).text

    def save(self):
        self.driver.find_element_by_xpath(self.SAVE_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.TIP)))


class ApplicationPopup(Component):
    SHOW_APP_RADIO_BUTTON = '//*[@id="field_place_PORTLET"]'
    INSTALL_BUTTON = '//*[@id="hook_FormButton_button_install"]'
    APP_NAME = '//*[@id="field_name"]'
    POPUP_WINDOW = '//*[@id="popLayer_mo"]'

    def __init__(self, driver):
        super(ApplicationPopup, self).__init__(driver)
        el = self.driver.find_element_by_xpath(self.APP_NAME)
        self.app_name = el.get_attribute('value')

    def apply_install(self):
        self.driver.find_element_by_xpath(self.SHOW_APP_RADIO_BUTTON).click()
        self.driver.find_element_by_xpath(self.INSTALL_BUTTON).click()
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element_located((By.XPATH, self.POPUP_WINDOW)))
        return self


class AddGroupLinksPopup(Component):
    POPUP = '//*[@id="popLayer_mo"]'
    SELECT = '//*[@id="hook_InviteChangeCard_4585283105"]/div/div[2]/div[2]/div[2]/div[2]'
    ADD_BUTTON = '//*[@id="hook_FormButton_button_invite"]'

    def add(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, self.POPUP)))
        self.driver.execute_script(
            "document.getElementsByClassName('ifSelect')[0].style.display = 'block';")
        self.driver.find_element_by_xpath(self.SELECT).click()
        self.driver.find_element_by_xpath(self.ADD_BUTTON).click()


class ApplicationForm(Component):
    APPLICATION = '//*[@id="availableApps"]/div[2]/div/div[1]/div[2]/div/div[3]/a'

    def install_app(self):
        self.driver.find_element_by_xpath(self.APPLICATION).click()
        return ApplicationPopup(self.driver)


class ManagmentForm(Component):
    GENERATE_API_KEY_BUTTON = '//*[@id="group-settings-form"]/div[8]/div[2]/div/div[2]/div/a'
    API_KEY_INPUT = '//*[@id="hook_Form_PopLayerAltGroupChangeTokenForm"]/form/input[3]'

    def generate_api_key(self):
        self.driver.find_element_by_xpath(self.GENERATE_API_KEY_BUTTON).click()
        return self.driver.find_element_by_xpath(self.API_KEY_INPUT).value


class PopupUserMenu(Component):
    ASSIGN_MODERATOR_POPUP_ITEM = '//*[@id="hook_Block_MainContainer"]/div[5]/table/tbody/tr/td/div/div/div[1]/div/ul[2]/li[2]'
    REMOVE_MODERATOR_POPUP_ITEM = '//*[@id="hook_Block_MainContainer"]/div[5]/table/tbody/tr/td/div/div/div[1]/div/ul[2]/li[4]'

    @property
    def assign_as_moderator(self) -> ModerForm:
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.ASSIGN_MODERATOR_POPUP_ITEM))).click()
        return ModerForm(self.driver)

    @property
    def remove_as_moderator(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.REMOVE_MODERATOR_POPUP_ITEM))).click()
        return ModerForm(self.driver)
