from pages.group_components import LeftActionBar
from pages.page import Page


class GroupPage(Page):

    @property
    def left_action_bar(self):
        return LeftActionBar(self.driver)

    def delete_group(self):
        self.left_action_bar.delete()
