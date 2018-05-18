from typing import List

from pages.album_components import AlbumControlPanel, ImageCard, PhotosPanel
from pages.page import Page


class AlbumPage(Page):

    @property
    def title(self) -> str:
        return self.control_panel.title

    @title.setter
    def title(self, new_title) -> None:
        self.control_panel.title = new_title

    @property
    def control_panel(self) -> AlbumControlPanel:
        return AlbumControlPanel(self.driver)

    @property
    def photos_panel(self) -> PhotosPanel:
        return PhotosPanel(self.driver)

    def delete_album(self) -> None:
        self.control_panel.delete_album()

    def upload_photo(self, path: str) -> ImageCard:
        return self.photos_panel.upload(path)

    def upload_photos(self, images: List[str]) -> List[ImageCard]:
        return self.photos_panel.bulk_upload(images)

    def image(self, image_id) -> ImageCard:
        return self.photos_panel.find_image(image_id)
