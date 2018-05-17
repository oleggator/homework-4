from pages.page import Page
from pages.settings_components import ApplicationForm


class ApplicationPage(Page):
    @property
    def form(self):
        return ApplicationForm(self.driver)

    def add_app(self):
        form = self.form
        return form.install_app().apply_install().app_name

