import os
import unittest
from typing import List

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.album_page import AlbumPage
from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.images_components import ImageCard
from pages.my_groups_components import GroupSubcategory, AgeRestriction
from pages.photo_components import AlbumType
from pages.photo_page import PhotoPage


class ImagesTransferTest(unittest.TestCase):
    TEST_GROUP: dict = {
        'description': 'test-auto-description',
        'title': 'test-auto-title',
        'subcategory': GroupSubcategory.ANIMALS,
        'age_restriction': AgeRestriction.NO_RESTRICTION,
    }

    SAMPLE_ALBUM: dict = {
        'title': 'test-auto-title',
        'admins_only': False,
        'sticky_album': False,
    }
    SAMPLE_OTHER_ALBUM: dict = {
        'title': 'test-auto-other-title',
        'admins_only': False,
        'sticky_album': False,
    }

    SAMPLE_IMAGE_PATH: str = 'assets/sample_image.jpg'
    SAMPLE_IMAGES_PACK: List[str] = ['assets/sample_image.jpg', 'assets/sample_image.jpg']

    @classmethod
    def setUpClass(cls):
        cls.browser: str = os.getenv('BROWSER', 'CHROME')
        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, cls.browser).copy()
        )
        login: str = os.environ.get('LOGIN')
        password: str = os.environ.get('PASSWORD')

        cls.group: GroupPage = AuthPage(cls.driver).open() \
            .sign_in(login, password) \
            .to_groups_page() \
            .create_public_page(cls.TEST_GROUP)
        cls.photo_page: PhotoPage = cls.group.to_photo_page()

        cls.albums = []

    def tearDown(self):
        for album in self.albums:
            album.open()
            album.delete_album()

        self.albums.clear()

    def add_album(self, album_description: dict) -> AlbumPage:
        album: AlbumPage = self.photo_page.open() \
            .create_album(AlbumType.ALBUM, album_description)
        self.albums.append(album)
        return album

    @classmethod
    def tearDownClass(cls):
        cls.group.open()
        cls.group.delete_group()
        cls.driver.quit()

    def test_single_image_transfer(self):
        main_album: AlbumPage = self.add_album(self.SAMPLE_ALBUM)
        other_album: AlbumPage = self.add_album(self.SAMPLE_OTHER_ALBUM)
        main_album.open()
        image: ImageCard = main_album.photos_panel.upload(self.SAMPLE_IMAGE_PATH)
        main_album.photos_panel.transfer_images([image], self.SAMPLE_OTHER_ALBUM['title'])
        other_album.open()
        self.assertEqual(1, len(other_album.photos_panel.images))

    def test_all_images_transfer(self):
        main_album: AlbumPage = self.add_album(self.SAMPLE_ALBUM)
        other_album: AlbumPage = self.add_album(self.SAMPLE_OTHER_ALBUM)
        main_album.open()
        main_album.photos_panel.bulk_upload(self.SAMPLE_IMAGES_PACK)
        main_album.photos_panel.transfer_all_images(self.SAMPLE_OTHER_ALBUM['title'])
        other_album.open()
        self.assertEqual(len(self.SAMPLE_IMAGES_PACK), len(other_album.photos_panel.images))
