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
    SAMPLE_TITLE: str = 'test-new-title'

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
        self.assertEqual({'reaction': Reaction.LIKE, 'counter': 1}, like.description)

    def test_album_like_wow(self):
        like: Like = self.album.control_panel.set_like(Reaction.WOW)
        self.assertEqual({'reaction': Reaction.WOW, 'counter': 1}, like.description)

    def test_album_like_heart(self):
        like: Like = self.album.control_panel.set_like(Reaction.HEART)
        self.assertEqual({'reaction': Reaction.HEART, 'counter': 1}, like.description)

    def test_album_like_sorrow(self):
        like: Like = self.album.control_panel.set_like(Reaction.SORROW)
        self.assertEqual({'reaction': Reaction.SORROW, 'counter': 1}, like.description)

    def test_album_like_lol(self):
        like: Like = self.album.control_panel.set_like(Reaction.LOL)
        self.assertEqual({'reaction': Reaction.LOL, 'counter': 1}, like.description)

    def test_album_like_unset(self):
        self.album.control_panel \
            .set_like(Reaction.LIKE) \
            .unset_like()
        like: Like = self.album.control_panel.like
        self.assertEqual({'reaction': Reaction.UNSET, 'counter': 0}, like.description)

    def test_album_change_title(self):
        self.album.title = self.SAMPLE_TITLE
        self.assertEqual(self.SAMPLE_TITLE, self.album.title)

    def test_album_change_to_empty_title(self):
        origin: str = self.ALBUM['title']
        self.album.title = ''
        self.assertEqual(origin, self.album.title)


