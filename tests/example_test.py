import unittest

import os
from selenium.webdriver import DesiredCapabilities, Remote

from pages.auth_page import AuthPage
from pages.my_groups_components import GroupPageCreateForm


class ExampleTest(unittest.TestCase):
    LOGIN = os.environ['LOGIN']
    PASSWORD = os.environ['PASSWORD']

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def test(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()

        profile_page = auth_page.sign_in(self.LOGIN, self.PASSWORD)

        desc = {
            'description': 'group about shit',
            'title': 'pulp fiction',
            'subcategory': GroupPageCreateForm.CINEMA_TV,
            'age_restriction': 0
        }

        group_page = profile_page.to_groups_page().create_public_page(desc)
        group_page.open()

        setting_page = group_page.to_settings_page()
        setting_page.to_admin_page()

        group_page.delete_group()
