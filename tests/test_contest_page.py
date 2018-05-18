import os
import unittest
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.album_components import Reaction, Like
from pages.contest_page import ContestPage
from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.my_groups_components import GroupSubcategory, AgeRestriction
from pages.photo_components import AlbumType
from pages.photo_page import PhotoPage


class ContestPageTest(unittest.TestCase):
    TILL_DATE: str = '{0}.{1}.{2}'.format(datetime.today().day, datetime.today().month, datetime.today().year + 1)
    SAMPLE_IMAGE_PATH: str = 'assets/sample_image.jpg'

    TEST_GROUP: dict = {
        'description': 'test-auto-description',
        'title': 'test-auto-title',
        'subcategory': GroupSubcategory.ANIMALS,
        'age_restriction': AgeRestriction.NO_RESTRICTION,
    }

    CONTEST: dict = {
        'title': 'test-auto-title',
        'description': "sample description",
        'till_date': TILL_DATE,
        'cover': SAMPLE_IMAGE_PATH,
        'admins_only': False,
        'sticky_album': False,
    }

    @classmethod
    def setUpClass(cls):
        cls.browser: str = os.getenv('BROWSER', 'CHROME')
        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, cls.browser).copy()
        )
        cls.driver.implicitly_wait(10)
        login: str = os.environ.get('LOGIN')
        password: str = os.environ.get('PASSWORD')

        cls.group: GroupPage = AuthPage(cls.driver).open() \
            .sign_in(login, password) \
            .to_groups_page() \
            .create_public_page(cls.TEST_GROUP)
        cls.photo_page: PhotoPage = cls.group.to_photo_page()

    def setUp(self):
        self.contest: ContestPage = self.photo_page.create_album(AlbumType.CONTEST, self.CONTEST)

    def tearDown(self):
        self.contest.open()
        self.contest.delete_album()

    @classmethod
    def tearDownClass(cls):
        cls.group.open()
        cls.group.delete_group()
        cls.driver.quit()

    def test_album_like(self):
        like: Like = self.contest.control_panel.set_like(Reaction.LIKE)
        like_result: Like = self.contest.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_wow(self):
        like: Like = self.contest.control_panel.set_like(Reaction.WOW)
        like_result: Like = self.contest.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_heart(self):
        like: Like = self.contest.control_panel.set_like(Reaction.HEART)
        like_result: Like = self.contest.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_sorrow(self):
        like: Like = self.contest.control_panel.set_like(Reaction.SORROW)
        like_result: Like = self.contest.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_lol(self):
        like: Like = self.contest.control_panel.set_like(Reaction.LOL)
        like_result: Like = self.contest.control_panel.like
        self.assertEqual(like.description, like_result.description)
