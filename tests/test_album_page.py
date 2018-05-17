import os
import unittest

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.album_components import Reaction, Like
from pages.album_page import AlbumPage
from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.my_groups_components import GroupSubcategory, AgeRestriction
from pages.photo_components import AlbumType
from pages.photo_page import PhotoPage


class AlbumPageTest(unittest.TestCase):
    TEST_GROUP: dict = {
        'description': 'test-auto-description',
        'title': 'test-auto-title',
        'subcategory': GroupSubcategory.ANIMALS,
        'age_restriction': AgeRestriction.NO_RESTRICTION,
    }

    ALBUM: dict = {
        'title': 'test-auto-title',
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
        self.album: AlbumPage = self.photo_page.create_album(AlbumType.ALBUM, self.ALBUM)

    def tearDown(self):
        self.album.open()
        self.album.delete_album()

    @classmethod
    def tearDownClass(cls):
        cls.group.open()
        cls.group.delete_group()
        cls.driver.quit()

    def test_album_like(self):
        like: Like = self.album.control_panel.set_like(Reaction.LIKE)
        like_result: Like = self.album.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_wow(self):
        like: Like = self.album.control_panel.set_like(Reaction.WOW)
        like_result: Like = self.album.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_heart(self):
        like: Like = self.album.control_panel.set_like(Reaction.HEART)
        like_result: Like = self.album.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_sorrow(self):
        like: Like = self.album.control_panel.set_like(Reaction.SORROW)
        like_result: Like = self.album.control_panel.like
        self.assertEqual(like.description, like_result.description)

    def test_album_like_lol(self):
        like: Like = self.album.control_panel.set_like(Reaction.LOL)
        like_result: Like = self.album.control_panel.like
        self.assertEqual(like.description, like_result.description)
