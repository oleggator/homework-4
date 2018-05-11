from urllib import parse

from pages.group_page import GroupPage
from pages.my_groups_components import GroupCreateDialog, GroupCreateButton
from pages.page import Page


class MyGroupsPage(Page):

    def create_public_page(self, description: dict) -> GroupPage:
        self.group_create_button.click()
        create_dialog = GroupCreateDialog(self.driver)
        create_dialog.choose_public_page(description)
        path = parse.urlparse(self.driver.current_url).path
        return GroupPage(self.driver, path=path)

    @property
    def group_create_button(self) -> GroupCreateButton:
        return GroupCreateButton(self.driver)
