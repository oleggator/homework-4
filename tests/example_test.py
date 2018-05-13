import os
import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.my_groups_components import GroupPageCreateForm
from pages.settings_components import GeneralForm


class ExampleTest(unittest.TestCase):
    LOGIN_1 = os.environ['LOGIN_1']
    PASSWORD_1 = os.environ['PASSWORD_1']
    LOGIN_2 = os.environ['LOGIN_2']
    PASSWORD_2 = os.environ['PASSWORD_2']

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver_1 = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.driver_1.implicitly_wait(10)

        self.driver_2 = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.driver_2.implicitly_wait(10)
        auth_page = AuthPage(self.driver_1)
        auth_page.open()

        profile_page = auth_page.sign_in(self.LOGIN_1, self.PASSWORD_1)

        desc = {
            'description': 'group about shit',
            'title': 'pulp fiction',
            'subcategory': GroupPageCreateForm.CINEMA_TV,
            'age_restriction': 0
        }

        group_page = profile_page.to_groups_page().create_public_page(desc)
        group_page.open()

        auth_page_user2 = AuthPage(self.driver_2)
        auth_page_user2.open()

        profile_user_2 = auth_page_user2.sign_in(self.LOGIN_2, self.PASSWORD_2)
        group_page_user2 = GroupPage(self.driver_2, path=group_page.path).open()
        group_page_user2.join()

        setting_page = group_page.to_settings_page()

        self.group_page = group_page
        self.setting_page = setting_page
        self.profile_user_2 = profile_user_2

    def tearDown(self):
        self.group_page.delete_group()
        self.driver_1.quit()
        self.driver_2.quit()

    def test_add_moderator(self):
        admin_page = self.setting_page.to_admin_page()
        admin_page.add_moderator(self.profile_user_2.name). \
            assign_as_moderator. \
            add_grant()
        admin_page.to_administration_list()
        self.assertTrue(admin_page.is_exists_moder_href(self.profile_user_2.name))

    def test_change_name_and_descriptions(self):
        general_page = self.setting_page.to_general_page()
        general_page.change_name_and_description('kill bill', "this group about bill's death")
        self.group_page.open()
        self.assertEqual(self.group_page.get_name(), 'kill bill')
        self.assertEqual(self.group_page.get_description(), "this group about bill's death")

    def test_chane_groups_category(self):
        general_page = self.setting_page.to_general_page()
        general_page.change_category_of_group(GeneralForm.Categories.STAR.value)
        form = general_page.form
        type = form.type
        category = form.category
        self.group_page.open()
        self.assertEqual("{}, {}".format(type, category), self.group_page.get_category())
