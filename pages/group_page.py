from pages.group_components import LeftActionBar, MainNavBar
from pages.page import Page
from pages.photo_page import PhotoPage
from pages.settings_page import SettingsPage


class GroupPage(Page):

    @property
    def left_action_bar(self) -> LeftActionBar:
        return LeftActionBar(self.driver)

    @property
    def main_nav_bar(self) -> MainNavBar:
        return MainNavBar(self.driver)

    def to_photo_page(self) -> PhotoPage:
        photo_page = self.main_nav_bar.photo_page
        photo_page.open()
        return photo_page

    def to_settings_page(self) -> SettingsPage:
        setting_page = self.left_action_bar.to_settings_page
        setting_page.open()
        return setting_page

    def delete_group(self):
        self.left_action_bar.delete()
