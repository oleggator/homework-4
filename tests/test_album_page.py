import os
import unittest
from typing import List

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.album_components import ImageCard
from pages.album_page import AlbumPage
from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.my_groups_components import GroupSubcategory, AgeRestriction
from pages.photo_components import AlbumType
from pages.photo_page import PhotoPage


class AlbumPageCreationTest(unittest.TestCase):
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

    ALBUM_FOR_ADMINS: dict = {
        'title': 'test-auto-title',
        'admins_only': True,
        'sticky_album': False,
    }

    STICKY_ALBUM: dict = {
        'title': 'test-auto-title',
        'admins_only': True,
        'sticky_album': False,
    }

    def setUp(self):
        self.browser: str = os.getenv('BROWSER', 'CHROME')
        self.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, self.browser).copy()
        )
        self.driver.implicitly_wait(10)
        login: str = os.environ.get('LOGIN')
        password: str = os.environ.get('PASSWORD')

        self.group: GroupPage = AuthPage(self.driver).open() \
            .sign_in(login, password) \
            .to_groups_page() \
            .create_public_page(self.TEST_GROUP)
        self.photo_page: PhotoPage = self.group.to_photo_page()

    def test_album_creation(self):
        album: AlbumPage = self.photo_page.create_album(AlbumType.ALBUM, self.ALBUM)
        self.assertEqual(self.ALBUM['title'], album.title)

    def test_album_for_admins_creation(self):
        album: AlbumPage = self.photo_page.create_album(AlbumType.ALBUM, self.ALBUM_FOR_ADMINS)
        # TODO: check access right
        self.assertEqual(self.ALBUM_FOR_ADMINS['title'], album.title)

    def test_sticky_album_creation(self):
        album: AlbumPage = self.photo_page.create_album(AlbumType.ALBUM, self.STICKY_ALBUM)
        # TODO: check sticky album
        self.assertEqual(self.STICKY_ALBUM['title'], album.title)

    def tearDown(self):
        self.group.open()
        self.group.delete_group()
        self.driver.quit()


class AlbumPageImageUploadTest(unittest.TestCase):
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

    SAMPLE_IMAGE_PATH: str = 'assets/sample_image.jpg'
    SAMPLE_BIG_IMAGE_PATH: str = 'assets/sample_big_image.jpg'
    SAMPLE_SMALL_IMAGE_PATH: str = 'assets/sample_small_image.jpg'
    SAMPLE_BULK_IMAGES: List[str] = ['assets/sample_image.jpg' for x in range(0, 10)]

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
        self.album: AlbumPage = self.photo_page.open() \
            .create_album(AlbumType.ALBUM, self.ALBUM)

    def tearDown(self):
        self.album.open()
        self.album.delete_album()

    @classmethod
    def tearDownClass(cls):
        cls.group.open()
        cls.group.delete_group()
        cls.driver.quit()

    def test_image_upload(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_IMAGE_PATH)
        uploaded: ImageCard = self.album.photos_panel.get_last()
        self.assertEqual(image.id, uploaded.id)

    def test_big_image_upload(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_BIG_IMAGE_PATH)
        uploaded: ImageCard = self.album.photos_panel.get_last()
        self.assertEqual(image.id, uploaded.id)

    def test_small_image_upload(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_SMALL_IMAGE_PATH)
        uploaded: ImageCard = self.album.photos_panel.get_last()
        self.assertEqual(image.id, uploaded.id)

    @unittest.skipIf(os.getenv('BROWSER', 'CHROME') == 'FIREFOX',
                     "simple multiply images upload way was not working in firefox")
    def test_bulk_image_upload(self):
        images: List[ImageCard] = self.album.upload_photos(self.SAMPLE_BULK_IMAGES)
        uploaded: List[ImageCard] = self.album.photos_panel.images
        self.assertEqual(len(images), len(uploaded))
