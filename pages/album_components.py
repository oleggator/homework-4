import os
from enum import Enum
from typing import List, Optional
from urllib import parse

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages import waits
from pages.images_components import ImageCard, ConfirmMakeMainModal
from pages.page import Component
from pages.photo_components import AlbumCreateModalForm
from pages.waits import web_element_locator, button_locator


class AlbumDeleteConfirmModal(Component):
    CONFIRM: str = '//input[@id="hook_FormButton_button_remove_confirm"]'
    CANCEL: str = '//input[@id="button_cancel_confirm"]'

    def confirm(self) -> None:
        self.confirm_button.click()

    def cancel(self) -> None:
        self.cancel_button.click()

    @property
    @web_element_locator((By.XPATH, CONFIRM))
    def confirm_button(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.CONFIRM)

    @property
    @web_element_locator((By.XPATH, CANCEL))
    def cancel_button(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.CANCEL)


class Reaction(Enum):
    WOW = '__react-wow'
    HEART = '__react-heart'
    LOL = '__react-lol'
    SORROW = '__react-sorrow'
    LIKE = '__react-like'
    UNSET = ''


class Like(Component):
    LIKE_DISABLED: str = "//span[@data-type='GROUP_ALBUM']/ancestor::*[starts-with(@id, 'hook_Block')][1]"
    LIKE_ENABLED: str = "//div[@class='__vis']"
    LIKE_BUTTON_TEMPLATE: str = '#hook_Block_ShortcutMenuReact .{} ~ .reaction_icw'
    LIKE_COUNT: str = '.widget_count'
    LABEL: str = 'span[data-type="GROUP_ALBUM"] .widget_tx'
    REACTION_LABEL: str = '.widget_tx.{}'

    def __init__(self, driver):
        super().__init__(driver)
        self.reactions_mapping = {reaction.value: reaction for reaction in Reaction}
        self.TOGGLE = self.LIKE_DISABLED

    def set_like(self, reaction: Reaction = Reaction.LIKE):
        like, selector = self.get_reaction_button(reaction)
        ActionChains(self.driver).move_to_element(like).click().perform()
        self.disable_likes()

    def unset_like(self):
        current: Reaction = self.reaction
        if current == Reaction.UNSET:
            return
        ActionChains(self.driver).move_to_element(self.like_toggle_button).click().perform()
        WebDriverWait(self.driver, 10).until(
            waits.element_not_found_by_css_selector(self.REACTION_LABEL.format(current.value))
        )

    @property
    def like_toggle_button(self):
        return self.driver.find_element_by_xpath(self.TOGGLE)

    def generate_like_button_selector(self, reaction: Reaction) -> str:
        return self.LIKE_BUTTON_TEMPLATE.format(reaction.value)

    def get_reaction_button(self, reaction: Reaction) -> (WebElement, str):
        button_selector: str = self.generate_like_button_selector(reaction)
        self.enable_likes(button_selector)
        return self.driver.find_element_by_css_selector(button_selector), button_selector

    def enable_likes(self, selector: str):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, self.TOGGLE))
        )
        self.driver.execute_script('''
            let mouseenter = new Event('mouseenter');    
            let node = document.evaluate("{}",document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
            document.querySelector('.ic_klass').dispatchEvent(mouseenter)
            node.dispatchEvent(mouseenter);
        '''.format(self.TOGGLE))

        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        self.TOGGLE = self.LIKE_ENABLED

    def disable_likes(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, self.TOGGLE))
        )
        self.driver.execute_script('''
            let mouseleave = new Event('mouseleave');    
            let node = document.evaluate("{}",document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;            
            node.dispatchEvent(mouseleave);
        '''.format(self.TOGGLE))
        self.TOGGLE = self.LIKE_DISABLED
        WebDriverWait(self.driver, 10).until(
            waits.element_not_found_by_xpath(self.LIKE_ENABLED)
        )

    @property
    def description(self) -> dict:
        return {
            'reaction': self.reaction,
            'counter': self.like_counter
        }

    @property
    @web_element_locator((By.CSS_SELECTOR, LIKE_COUNT))
    def like_counter_elem(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.LIKE_COUNT)

    @property
    def like_counter(self) -> int:
        counter: str = self.like_counter_elem.text
        return int(counter)

    @property
    def reaction(self) -> Reaction:
        reaction_class_list: str = self.label.get_attribute('class')
        reaction_class: str = reaction_class_list.replace('widget_tx', '').strip()
        if reaction_class == '':
            return Reaction.UNSET
        return self.reactions_mapping.get(reaction_class, Reaction.UNSET)

    @property
    @web_element_locator((By.CSS_SELECTOR, LABEL))
    def label(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.LABEL)


class AlbumControlPanel(Component):
    DELETE: str = 'ul.controls-list > li:nth-child(2) > a'
    EDIT: str = '.photo-menu_edit a'
    BACK: str = '.ic12.ic12_answer'
    TITLE: str = 'span.photo-h_cnt_t'
    TITLE_EDIT: str = '.it.h-mod'

    MAIN_PHOTO: str = '.photo-panel_cover img'

    def __init__(self, driver):
        super().__init__(driver)

    def delete_album(self) -> None:
        self.edit_button.click()
        self.delete_button.click()
        AlbumDeleteConfirmModal(self.driver).confirm()

    @property
    @button_locator((By.CSS_SELECTOR, DELETE))
    def delete_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DELETE)

    @property
    @button_locator((By.CSS_SELECTOR, EDIT))
    def edit_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.EDIT)

    @property
    @button_locator((By.CSS_SELECTOR, BACK))
    def back_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.BACK)

    def enable_edit(self):
        edit_button_wrapper: List[WebElement] = self.driver.find_elements_by_css_selector(self.EDIT)
        if len(edit_button_wrapper) == 0:
            return
        self.edit_button.click()
        waits.wait(self.driver) \
            .until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.BACK))
        )

    @property
    @web_element_locator((By.CSS_SELECTOR, TITLE))
    def title(self) -> str:
        return self.driver.find_element_by_css_selector(self.TITLE).text

    @property
    @web_element_locator((By.CSS_SELECTOR, TITLE_EDIT))
    def title_input(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.TITLE_EDIT)

    @title.setter
    def title(self, new_title):
        self.enable_edit()
        self.title_input.clear()
        self.title_input.send_keys(new_title)
        self.disable_edit()

    def set_like(self, reaction: Reaction):
        like: Like = Like(self.driver)
        like.set_like(reaction)
        return like

    @property
    def like(self):
        return Like(self.driver)

    def disable_edit(self):
        back_button_wrapper: List[WebElement] = self.driver.find_elements_by_css_selector(self.BACK)
        if len(back_button_wrapper) == 0:
            return
        self.back_button.click()
        waits.wait(self.driver) \
            .until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.EDIT))
        )

    @property
    @web_element_locator((By.CSS_SELECTOR, MAIN_PHOTO))
    def main_img_raw(self):
        return self.driver.find_element_by_css_selector(self.MAIN_PHOTO)

    @property
    def main_photo(self) -> ImageCard:
        img_id: str = id_from_src(self.main_img_raw.get_attribute('src'))
        return ImageCard(self.driver, img_id)

    @main_photo.setter
    def main_photo(self, new_main_photo: ImageCard):
        self.request_main_photo(new_main_photo).confirm()

    def request_main_photo(self, new_main_photo: ImageCard) -> ConfirmMakeMainModal:
        modal: ConfirmMakeMainModal = new_main_photo.make_main()

        main_photo_change = self.create_main_photo_change_waiter(new_main_photo.id)

        modal.on_confirm = lambda: waits.wait(self.driver).until(main_photo_change)
        return modal

    def commit_changes(self) -> None:
        self.disable_edit()

    def create_main_photo_change_waiter(self, new_id):
        def waiter(driver):
            main_photo: WebElement = driver.find_element_by_css_selector(self.MAIN_PHOTO)
            try:
                found_id: str = id_from_src(main_photo.get_attribute('src'))
                if found_id == new_id:
                    return main_photo
            except StaleElementReferenceException:
                return False
            return False

        return waiter


class TransferAlbumDropdown(Component):
    TRANSFER_TARGET_TEMPLATE: str = '//div[@class="custom-isl_drop-lst"]/descendant::a[text()="{}"]'
    DROPDOWN: str = '.dropDownListContentWrapper'
    CREATE_TRANSFER_TARGET: str = '.custom-isl_drop-lst a.custom-isl_i_l.al.ellip'
    START_TRANSFER: str = '.js-button_move'
    ACKNOWLEDGEMENT: str = '.iblock.__ok'

    def choose(self, album_name: str):
        self.dropdown.click()
        transfer_target = self.get_transfer_target(album_name)
        transfer_target.click()
        self.start_transfer()
        waits.wait(self.driver).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.ACKNOWLEDGEMENT))
        )

    @property
    @web_element_locator((By.CSS_SELECTOR, CREATE_TRANSFER_TARGET))
    def create_new_album_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.CREATE_TRANSFER_TARGET)

    @property
    @web_element_locator((By.CSS_SELECTOR, DROPDOWN))
    def dropdown(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DROPDOWN)

    def get_transfer_target(self, album_name) -> WebElement:
        transfer_target = self.TRANSFER_TARGET_TEMPLATE.format(album_name)
        waits.wait(self.driver).until(expected_conditions.presence_of_element_located((By.XPATH, transfer_target)))
        return self.driver.find_element_by_xpath(transfer_target)

    def choose_new(self, album_description: dict):
        self.create_new_album_button.click()
        AlbumCreateModalForm(self.driver, album_description).submit()

    def start_transfer(self):
        self.start_transfer_button.click()

    @property
    @button_locator((By.CSS_SELECTOR, START_TRANSFER))
    def start_transfer_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.START_TRANSFER)


class PhotosPanel(Component):
    LOADER: str = "//div[@class='photo-card_loading']"

    PHOTOS: str = '.photo-card_cnt img'
    UPLOADED_PHOTOS: str = '//li[@class="ugrid_i"]/div[starts-with(@id, "hook_Block_UploadedGroupPhotoCardBlock")]'
    SELECT_ALL: str = '#checkboxSelAll'
    UPLOAD: str = '//input[@name="photo"]'
    IMAGE_LOCATOR: str = '#img_{}'

    @property
    @web_element_locator((By.CSS_SELECTOR, PHOTOS))
    def images(self) -> List[WebElement]:
        return self.driver.find_elements_by_css_selector(self.PHOTOS)

    @property
    @web_element_locator((By.XPATH, UPLOAD))
    def upload_input(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.UPLOAD)

    def get_first(self):
        id_img: str = ''
        if self.driver.name.lower() == 'firefox':
            id_img = id_from_web_element(self.images[-1])
        else:
            id_img = id_from_web_element(self.images[0])
        return ImageCard(self.driver, id_img)

    def get_last(self):
        id_img: str = ''
        if self.driver.name.lower() == 'firefox':
            id_img = id_from_web_element(self.images[0])
        else:
            id_img = id_from_web_element(self.images[-1])
        return ImageCard(self.driver, id_img)

    def transfer_images(self, images: List[ImageCard], dest: str):
        for image in images:
            image.check()
        TransferAlbumDropdown(self.driver).choose(dest)

    def upload(self, path: str, current=0) -> ImageCard:
        path = os.path.abspath(path)
        self.upload_input.send_keys(path)
        self.wait_uploading(current + 1)
        return self.get_first()

    def wait_uploading(self, count=1) -> None:
        waits.wait(self.driver).until(
            waits.number_of_elements_located((By.XPATH, self.UPLOADED_PHOTOS), count)
        )

    def bulk_upload(self, images: List[str]) -> List[ImageCard]:
        if self.driver.name.lower() == 'firefox':
            uploading = 0
            uploaded = []
            for path in images:
                uploaded.append(self.upload(os.path.abspath(path), uploading))
                uploading = uploading + 1
            return uploaded

        paths: str = '\n'.join([os.path.abspath(path) for path in images])
        self.upload_input.send_keys(paths)
        self.wait_uploading(len(images))
        return [ImageCard(self.driver, id_from_web_element(img)) for img in self.images]

    def find_image(self, image_id) -> Optional[ImageCard]:
        image_wrapper: List[ImageCard] = self.driver.find_elements_by_css_selector(self.IMAGE_LOCATOR.format(image_id))
        if len(image_wrapper) == 0:
            return None
        return image_wrapper[0]

    def transfer_all_images(self, dest):
        self.select_all_checkbox.click()
        TransferAlbumDropdown(self.driver).choose(dest)

    @property
    @button_locator((By.CSS_SELECTOR, SELECT_ALL))
    def select_all_checkbox(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.SELECT_ALL)


def id_from_web_element(img: WebElement) -> str:
    return img.get_attribute('id').replace('img_', '')


def id_from_src(src: str) -> str:
    query: str = parse.urlparse(src).query
    id_param: dict = parse.parse_qs(query)
    return id_param['id'][0]
