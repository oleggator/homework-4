from pages.page import Page
from pages.settings_components import ManagmentForm


class ManagmentPage(Page):

    @property
    def form(self):
        return ManagmentForm(self.driver)

    def generate_access_key(self):
        self.form.generate_api_key()
