from pages.page import Component


class AuthForm(Component):
    LOGIN = '//input[@name="st.email"]'
    PASSWORD = '//input[@name="st.password"]'
    SUBMIT = '//input[@type="submit"][@data-l="t,sign_in"]'

    @property
    def login(self):
        return self.driver.find_element_by_xpath(self.LOGIN).value()

    @login.setter
    def login(self, val):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(val)

    @property
    def password(self):
        return self.driver.find_element_by_xpath(self.PASSWORD).value()

    @password.setter
    def password(self, val):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(val)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()