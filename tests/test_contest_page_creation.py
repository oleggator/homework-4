import os
import unittest
from datetime import datetime
from typing import List

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.album_components import ImageCard
from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.my_groups_components import GroupSubcategory, AgeRestriction
from pages.photo_components import AlbumType
from pages.photo_page import PhotoPage
from pages.contest_page import ContestPage


class ContestPageCreationTest(unittest.TestCase):
    SAMPLE_IMAGE_PATH: str = 'assets/sample_image.jpg'
    TILL_DATE: str = '{0}.{1}.{2}'.format(datetime.today().day, datetime.today().month, datetime.today().year + 1)

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

    CONTEST_FOR_ADMINS: dict = {
        'title': 'test-auto-title',
        'description': "sample description",
        'till_date': TILL_DATE,
        'cover': SAMPLE_IMAGE_PATH,
        'admins_only': True,
        'sticky_album': False,
    }

    STICKY_CONTEST: dict = {
        'title': 'test-auto-title',
        'description': "sample description",
        'till_date': TILL_DATE,
        'cover': SAMPLE_IMAGE_PATH,
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

    def test_contest_creation(self):
        contest: ContestPage = self.photo_page.create_album(AlbumType.CONTEST, self.CONTEST)
        self.assertEqual(self.CONTEST['title'], contest.title)

    def test_contest_for_admins_creation(self):
        contest: ContestPage = self.photo_page.create_album(AlbumType.CONTEST, self.CONTEST_FOR_ADMINS)
        # TODO: check access right
        self.assertEqual(self.CONTEST_FOR_ADMINS['title'], contest.title)

    def test_sticky_contest_creation(self):
        contest: ContestPage = self.photo_page.create_album(AlbumType.CONTEST, self.STICKY_CONTEST)
        # TODO: check sticky contest
        self.assertEqual(self.STICKY_CONTEST['title'], contest.title)

    def tearDown(self):
        self.group.open()
        self.group.delete_group()
        self.driver.quit()


class ContestPageImageUploadTest(unittest.TestCase):
    TILL_DATE: str = '{0}.{1}.{2}'.format(datetime.today().day, datetime.today().month, datetime.today().year + 1)

    SAMPLE_IMAGE_PATH: str = 'assets/sample_image.jpg'
    SAMPLE_BIG_IMAGE_PATH: str = 'assets/sample_big_image.jpg'
    SAMPLE_SMALL_IMAGE_PATH: str = 'assets/sample_small_image.jpg'
    SAMPLE_BULK_IMAGES: List[str] = ['assets/sample_image.jpg' for x in range(0, 10)]

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
        self.contest: ContestPage = self.photo_page.open() \
            .create_album(AlbumType.CONTEST, self.CONTEST)

    def tearDown(self):
        self.contest.open()
        self.contest.delete_album()

    @classmethod
    def tearDownClass(cls):
        cls.group.open()
        cls.group.delete_group()
        cls.driver.quit()

    def test_image_upload(self):
        image: ImageCard = self.contest.upload_photo(self.SAMPLE_IMAGE_PATH)
        uploaded: ImageCard = self.contest.photos_panel.get_last()
        self.assertEqual(image.id, uploaded.id)

    def test_big_image_upload(self):
        image: ImageCard = self.contest.upload_photo(self.SAMPLE_BIG_IMAGE_PATH)
        uploaded: ImageCard = self.contest.photos_panel.get_last()
        self.assertEqual(image.id, uploaded.id)

    def test_small_image_upload(self):
        image: ImageCard = self.contest.upload_photo(self.SAMPLE_SMALL_IMAGE_PATH)
        uploaded: ImageCard = self.contest.photos_panel.get_last()
        self.assertEqual(image.id, uploaded.id)

    @unittest.skipIf(os.getenv('BROWSER', 'CHROME') == 'FIREFOX',
                     "simple multiply images upload way was not working in firefox")
    def test_bulk_image_upload(self):
        images: List[ImageCard] = self.contest.upload_photos(self.SAMPLE_BULK_IMAGES)
        uploaded: List[ImageCard] = self.contest.photos_panel.images
        self.assertEqual(len(images), len(uploaded))
