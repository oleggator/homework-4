from urllib import parse

from pages.album_page import AlbumPage
from pages.page import Page
from pages.photo_components import AlbumCreateButton, AlbumType


class PhotoPage(Page):

    def create_album(self, album_type: AlbumType, description: dict) -> AlbumPage:
        AlbumCreateButton(self.driver).create_album(album_type, description)
        path: str = parse.urlparse(self.driver.current_url).path
        return AlbumPage(self.driver, path=path)
