from selenium.webdriver.support.select import Select

from pages.page import Component, url_changer


class GroupCreateButton(Component):
    BUTTON = '//div[@class="create-group"]'

    def click(self):
        self.driver.find_element_by_xpath(self.BUTTON).click()


class GroupCreateDialog(Component):
    PAGE = '//a[@data-l="t,PAGE"]'
    INTEREST = '//a[@data-l="t,INTEREST"]'

    @property
    def page(self):
        return self.driver.find_element_by_xpath(self.PAGE)

    @property
    def interest(self):
        return self.driver.find_element_by_xpath(self.INTEREST)

    def choose_public_page(self, page_description):
        self.page.click()
        form = GroupPageCreateForm(self.driver, page_description)
        form.submit()


class GroupPageCreateForm(Component):
    TITLE = '//input[@name="st.layer.name"]'
    DESCRIPTION = '//textarea[@name="st.layer.description"]'
    SUBCATEGORY = '//select[@name="st.layer.pageMixedCategory"]'
    AGE_RESTRICTION = '//select[@name="st.layer.ageRestriction"]'
    SUBMIT = '//input[@name="button_create"]'
    CANCEL = '//a[@id="button_cancel"]'

    AUTO_MOTO = 'subcatVal12001'
    BLOG = 'subcatVal12001'
    CHILDREN = 'subcatVal12003'
    DESIGN = 'subcatVal12004'
    ANIMALS = 'subcatVal12005'
    GAMES = 'subcatVal12006'
    CINEMA_TV = 'subcatVal12007'
    BOOKS = 'subcatVal12008'
    IT = 'subcatVal12009'
    HEALTH = 'subcatVal12010'

    def __init__(self, driver, page_description):
        super().__init__(driver)
        self.title = page_description['title']
        self.description = page_description['description']
        self.subcategory = page_description['subcategory']
        self.isAdult = page_description['age_restriction']

    @property
    def title(self):
        return self.driver.find_element_by_xpath(self.TITLE)

    @title.setter
    def title(self, value):
        self.title.send_keys(value)

    @property
    def description(self):
        return self.driver.find_element_by_xpath(self.DESCRIPTION)

    @description.setter
    def description(self, value):
        self.description.send_keys(value)

    @property
    def subcategory(self):
        return Select(self.driver.find_element_by_xpath(self.SUBCATEGORY))

    @subcategory.setter
    def subcategory(self, value):
        self.subcategory.select_by_value(value)

    @property
    def age_restriction(self):
        return Select(self.driver.find_element_by_xpath(self.AGE_RESTRICTION))

    @age_restriction.setter
    def age_restriction(self, value):
        self.age_restriction.select_by_value(value)

    @url_changer
    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()

    def cancel(self):
        self.driver.find_element_by_xpath(self.CANCEL).click()
