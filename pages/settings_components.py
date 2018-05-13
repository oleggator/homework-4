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
