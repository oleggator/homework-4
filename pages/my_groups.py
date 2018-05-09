from pages.group_page import GroupPage
from pages.my_groups_components import GroupCreateDialog, GroupCreateButton
from pages.page import Page


class MyGroupsPage(Page):

    def create_page(self, description):
        self.group_create_button.click()
        create_dialog = GroupCreateDialog(self.driver)
        create_dialog.create_page(description)
        return GroupPage(self.driver, auto_path=True)

    @property
    def group_create_button(self):
        return GroupCreateButton(self.driver)
