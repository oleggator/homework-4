from enum import Enum

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from pages.page import Component, url_changer


class GroupCreateButton(Component):
    BUTTON: str = '//div[@class="create-group"]'

    def click(self):
        self.driver.find_element_by_xpath(self.BUTTON).click()


class GroupCreateDialog(Component):
    PAGE: str = '//a[@data-l="t,PAGE"]'
    INTEREST: str = '//a[@data-l="t,INTEREST"]'

    @property
    def page(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.PAGE)

    @property
    def interest(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.INTEREST)

    def choose_public_page(self, page_description):
        self.page.click()
        form: GroupPageCreateForm = GroupPageCreateForm(self.driver, page_description)
        form.submit()


class AgeRestriction(Enum):
    NO_RESTRICTION = 0,
    ADULT = 18


class GroupPageCreateForm(Component):
    TITLE: str = '//input[@name="st.layer.name"]'
    DESCRIPTION: str = '//textarea[@name="st.layer.description"]'
    SUBCATEGORY: str = '//select[@name="st.layer.pageMixedCategory"]'
    AGE_RESTRICTION: str = '//select[@name="st.layer.ageRestriction"]'
    SUBMIT: str = '//input[@name="button_create"]'
    CANCEL: str = '//a[@id="button_cancel"]'

    AUTO_MOTO: str = 'subcatVal12001'
    BLOG: str = 'subcatVal12001'
    CHILDREN: str = 'subcatVal12003'
    DESIGN: str = 'subcatVal12004'
    ANIMALS: str = 'subcatVal12005'
    GAMES: str = 'subcatVal12006'
    CINEMA_TV: str = 'subcatVal12007'
    BOOKS: str = 'subcatVal12008'
    IT: str = 'subcatVal12009'
    HEALTH: str = 'subcatVal12010'

    def __init__(self, driver, page_description: dict) -> None:
        super().__init__(driver)
        self.title = page_description['title']
        self.description = page_description['description']
        self.subcategory = page_description['subcategory']
        self.isAdult = page_description['age_restriction']

    @property
    def title(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.TITLE)

    @title.setter
    def title(self, value: str):
        self.title.send_keys(value)

    @property
    def description(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.DESCRIPTION)

    @description.setter
    def description(self, value: str):
        self.description.send_keys(value)

    @property
    def subcategory(self) -> Select:
        return Select(self.driver.find_element_by_xpath(self.SUBCATEGORY))

    @subcategory.setter
    def subcategory(self, value: str):
        self.subcategory.select_by_value(value)

    @property
    def age_restriction(self) -> Select:
        return Select(self.driver.find_element_by_xpath(self.AGE_RESTRICTION))

    @age_restriction.setter
    def age_restriction(self, value: AgeRestriction):
        self.age_restriction.select_by_value(value)

    @url_changer
    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()
