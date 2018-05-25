import os
import unittest
from typing import List

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from pages.album_page import AlbumPage
from pages.auth_page import AuthPage
from pages.group_page import GroupPage
from pages.images_components import ExpandedImageCard, ImageCard, ConfirmMakeMainModal
from pages.my_groups_components import GroupSubcategory, AgeRestriction
from pages.photo_components import AlbumType
from pages.photo_page import PhotoPage


class AlbumPageImagesManagementTest(unittest.TestCase):
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
    SAMPLE_IMAGE_DESCRIPTION: str = 'test-image-description'

    SAMPLE_IMAGE_PATH: str = 'assets/sample_image.jpg'
    SAMPLE_BIG_IMAGE_PATH: str = 'assets/sample_big_image.jpg'
    SAMPLE_SMALL_IMAGE_PATH: str = 'assets/sample_small_image.jpg'
    SAMPLE_IMAGES_PACK_BIG: List[str] = ['assets/sample_image.jpg' for x in range(0, 10)]
    SAMPLE_IMAGES_PACK_SMALL: List[str] = ['assets/sample_image.jpg' for x in range(0, 3)]
    SAMPLE_IMAGES_PACK_MEDIUM: List[str] = ['assets/sample_image.jpg', 'assets/sample_small_image.jpg',
                                            'assets/sample_big_image.jpg']

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

    def setUp(self):
        self.album: AlbumPage = self.photo_page.open() \
            .create_album(AlbumType.ALBUM, self.ALBUM)
        self.album_control_panel = self.album.control_panel
        self.album_photos_panel = self.album.photos_panel

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
        uploaded: ImageCard = self.album_photos_panel.get_first()
        self.assertEqual(image.id, uploaded.id)

    def test_big_image_upload(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_BIG_IMAGE_PATH)
        uploaded: ImageCard = self.album_photos_panel.get_first()
        self.assertEqual(image.id, uploaded.id)

    def test_small_image_upload(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_SMALL_IMAGE_PATH)
        uploaded: ImageCard = self.album_photos_panel.get_first()
        self.assertEqual(image.id, uploaded.id)

    def test_image_delete(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_IMAGE_PATH)
        image.delete_image_card()
        self.album_control_panel.commit_changes()
        self.assertIsNone(self.album.image(image.id))

    def test_set_image_description(self):
        image: ImageCard = self.album.upload_photo(self.SAMPLE_IMAGE_PATH)
        self.album_control_panel.enable_edit()
        image.description = self.SAMPLE_IMAGE_DESCRIPTION
        self.album_control_panel.disable_edit()
        expanded: ExpandedImageCard = image.expand()
        self.assertEquals(self.SAMPLE_IMAGE_DESCRIPTION, expanded.description)

    def test_make_main_image(self):
        self.album.upload_photos([self.SAMPLE_IMAGE_PATH, self.SAMPLE_IMAGE_PATH])
        self.album_control_panel.disable_edit()

        new_main_image: ImageCard = self.album_photos_panel.get_last()
        self.album_control_panel.main_photo = new_main_image
        main: ImageCard = self.album_control_panel.main_photo
        self.assertEqual(new_main_image.id, main.id)

    def test_cancel_make_main_image(self):
        self.album.upload_photos([self.SAMPLE_IMAGE_PATH, self.SAMPLE_IMAGE_PATH])
        self.album_control_panel.disable_edit()

        main_photo_candidate: ImageCard = self.album_photos_panel.get_last()
        current_main_id: str = self.album_control_panel.main_photo.id

        modal: ConfirmMakeMainModal = self.album_control_panel.request_main_photo(main_photo_candidate)
        modal.cancel()

        main_id: str = self.album_control_panel.main_photo.id

        self.assertEqual(main_id, current_main_id)

    def test_bulk_image_upload(self):
        images: List[ImageCard] = self.album.upload_photos(self.SAMPLE_IMAGES_PACK_BIG)
        uploaded: List[ImageCard] = self.album_photos_panel.images
        self.assertEqual(len(images), len(uploaded))

    @unittest.expectedFailure
    def test_restore_single_image(self):
        image: ImageCard = self.album_photos_panel.upload(self.SAMPLE_IMAGE_PATH)
        image_id = image.id
        image.delete_image_card()
        image.restore()
        self.album_control_panel.disable_edit()
        self.assertIsNotNone(self.album_photos_panel.find_image(image_id))

    def test_restore_one_image(self):
        images: List[ImageCard] = self.album.upload_photos(self.SAMPLE_IMAGES_PACK_BIG)
        images[0].delete_image_card()
        images[0].restore()
        self.album_control_panel.disable_edit()
        self.assertEqual(1, len(self.album_photos_panel.images))

    @unittest.expectedFailure
    def test_restore_all_images(self):
        images: List[ImageCard] = self.album.upload_photos(self.SAMPLE_IMAGES_PACK_SMALL)
        for image in images:
            image.delete_image_card()
            image.restore()
        self.album_control_panel.disable_edit()
        self.assertEqual(1, len(self.album_photos_panel.images))

    def test_images_reordering(self):
        self.album.upload_photos(self.SAMPLE_IMAGES_PACK_MEDIUM)
        images: List[ImageCard] = self.album_photos_panel.image_cards
        pushed_to_first_place_id = images[1].id
        self.album_photos_panel.drag_and_drop(images[0], images[-1])
        updated_images: List[ImageCard] = self.album_photos_panel.image_cards
        self.assertEqual(pushed_to_first_place_id, updated_images[0].id)

    def test_drag_and_drop_on_same_image(self):
        self.album.upload_photos(self.SAMPLE_IMAGES_PACK_MEDIUM)
        images: List[ImageCard] = self.album_photos_panel.image_cards
        first_id: str = images[0].id
        self.album_photos_panel.drag_and_drop(images[0], images[0])
        updated_images: List[ImageCard] = self.album_photos_panel.image_cards
        self.assertEqual(first_id, updated_images[0].id)
