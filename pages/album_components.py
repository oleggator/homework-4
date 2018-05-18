import os
from enum import Enum
from typing import List
from urllib import parse

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages import waits
from pages.page import Component


class AlbumDeleteConfirmModal(Component):
    CONFIRM: str = '//input[@id="hook_FormButton_button_remove_confirm"]'
    CANCEL: str = '//input[@id="button_cancel_confirm"]'

    def confirm(self) -> None:
        self.driver.find_element_by_xpath(self.CONFIRM).click()

    def cancel(self) -> None:
        self.driver.find_element_by_xpath(self.CANCEL).click()


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
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR, self.REACTION_LABEL.format(reaction.value)))
        )

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
    def like_counter(self) -> int:
        counter: str = self.driver.find_element_by_css_selector(self.LIKE_COUNT).text
        return int(counter)

    @property
    def reaction(self) -> Reaction:
        reaction_class_list: str = self.driver.find_element_by_css_selector(self.LABEL) \
            .get_attribute('class')
        reaction_class: str = reaction_class_list.replace('widget_tx', '').strip()
        if reaction_class == '':
            return Reaction.UNSET
        return self.reactions_mapping.get(reaction_class, Reaction.UNSET)


class AlbumControlPanel(Component):
    DELETE: str = 'ul.controls-list > li:nth-child(2) > a'
    EDIT: str = '.ic12_edit'
    BACK: str = '.ic12.ic12_answer'
    TITLE: str = 'span.photo-h_cnt_t'
    TITLE_EDIT: str = '.it.h-mod'

    def delete_album(self) -> None:
        self.edit_button.click()
        self.delete_button.click()
        AlbumDeleteConfirmModal(self.driver).confirm()

    @property
    def delete_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DELETE)

    @property
    def edit_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.EDIT)

    def enable_edit(self):
        edit_button_wrapper: List[WebElement] = self.driver.find_elements_by_css_selector(self.EDIT)
        if len(edit_button_wrapper) == 0:
            return
        edit_button_wrapper[0].click()
        waits.wait(self.driver) \
            .until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.BACK))
        )

    @property
    def title(self) -> str:
        return self.driver.find_element_by_css_selector(self.TITLE).text

    @property
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
        back_button_wrapper[0].click()
        waits.wait(self.driver) \
            .until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, self.EDIT))
        )


class ImageCard(Component):
    EDIT_TEMPLATE: str = '//div[@id="trigger_{}"]'
    DELETE_TEMPLATE: str = '#popup_{} .ic_delete'
    MAKE_MAIN_TEMPLATE: str = '#popup_{} .ic_make-main'
    EDIT_DESCRIPTION_TEMPLATE: str = '//[@id=descrInp{}]'

    def __init__(self, driver, src):
        super().__init__(driver)
        self.src = src
        query_string: str = parse.urlparse(self.src).query
        self.id: str = parse.parse_qs(query_string)['id'][0]
        self.EDIT_DESCRIPTION: str = self.EDIT_DESCRIPTION_TEMPLATE.format(self.id)
        self.EDIT: str = self.EDIT_TEMPLATE.format(self.id)
        self.DELETE: str = self.DELETE_TEMPLATE.format(self.id)
        self.MAKE_MAIN: str = self.MAKE_MAIN_TEMPLATE.format(self.id)

    @property
    def description(self) -> str:
        return self.driver.find_element_by_xpath(self.EDIT_DESCRIPTION).value()

    @property
    def edit(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.EDIT)

    @property
    def delete_button(self) -> WebElement:
        return self.driver.find_element_by_css_selector(self.DELETE)

    @description.setter
    def description(self, value) -> None:
        self.driver.find_element_by_xpath(self.EDIT_DESCRIPTION).send_keys(value)

    def make_main(self):
        pass

    def delete_image_card(self) -> None:
        self.driver.execute_script('''
            document.querySelector('{}').click()
        '''.format(self.DELETE))


class PhotosPanel(Component):
    LOADER: str = '//div[@class="photo-card_loading"]'
    PHOTOS: str = '.photo-card_cnt img'
    UPLOAD: str = '//input[@name="photo"]'

    def __init__(self, driver):
        super().__init__(driver)

    @property
    def images(self) -> List[WebElement]:
        return self.driver.find_elements_by_css_selector(self.PHOTOS)

    @property
    def upload_input(self) -> WebElement:
        return self.driver.find_element_by_xpath(self.UPLOAD)

    def get_last(self):
        src: str = self.images[0].get_attribute('src')
        return ImageCard(self.driver, src)

    def upload(self, path: str) -> ImageCard:
        path = os.path.abspath(path)
        self.driver.find_element_by_xpath(self.UPLOAD).send_keys(path)
        self.wait_uploading()
        return self.get_last()

    # TODO: rewrite due to performance issues
    def wait_uploading(self) -> None:
        WebDriverWait(self.driver, 60).until(
            waits.element_not_found_by_xpath((By.XPATH, self.LOADER))
        )

    def bulk_upload(self, images: List[str]) -> List[ImageCard]:
        upload_input: WebElement = self.upload_input
        paths: str = '\n'.join([os.path.abspath(path) for path in images])
        upload_input.send_keys(paths)
        self.wait_uploading()
        return [ImageCard(self.driver, img.get_attribute('src')) for img in self.images]
