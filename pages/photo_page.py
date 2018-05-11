from urllib import parse

from pages.album_page import AlbumPage
from pages.page import Page
from pages.photo_components import AlbumCreateButton


class PhotoPage(Page):

    def create_album(self, album_type, description):
        AlbumCreateButton(self.driver).create_album(album_type, description)
        path = parse.urlparse(self.driver.current_url).path
        return AlbumPage(self.driver, path=path)
