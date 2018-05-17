from pages.page import Component


class AuthForm(Component):
    LOGIN = '//input[@name="st.email"]'
    PASSWORD = '//input[@name="st.password"]'
    SUBMIT = '//input[@type="submit"][@data-l="t,sign_in"]'

    @property
    def login(self) -> str:
        return self.driver.find_element_by_xpath(self.LOGIN).text

    @login.setter
    def login(self, val):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(val)

    @property
    def password(self) -> str:
        return self.driver.find_element_by_xpath(self.PASSWORD).text

    @password.setter
    def password(self, val):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(val)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()
