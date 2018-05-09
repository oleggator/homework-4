from pages.group_components import LeftActionBar, MainNavBar
from pages.page import Page


class GroupPage(Page):

    @property
    def left_action_bar(self):
        return LeftActionBar(self.driver)

    @property
    def main_nav_bar(self):
        return MainNavBar(self.driver)

    def to_photo_page(self):
        photo_page = self.main_nav_bar.photo_page
        photo_page.open()
        return photo_page

    def delete_group(self):
        self.left_action_bar.delete()
