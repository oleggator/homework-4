from pages.auth_page_components import AuthForm
from pages.page import Page
from pages.profile_page import ProfilePage


class AuthPage(Page):

    @property
    def form(self):
        return AuthForm(self.driver)

    def sign_in(self, login, password):
        form = self.form
        form.login = login
        form.password = password
        form.submit()

        return ProfilePage(self.driver)
