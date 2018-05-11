from pages.my_groups import MyGroupsPage
from pages.page import Page
from pages.profile_components import LeftNavComponent


class ProfilePage(Page):

    @property
    def left_nav(self):
        return LeftNavComponent(self.driver)

    def to_groups_page(self) -> MyGroupsPage:
        my_groups_page: MyGroupsPage = self.left_nav.groups_page
        my_groups_page.open()
        return my_groups_page
