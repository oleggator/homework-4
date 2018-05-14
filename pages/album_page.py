from pages.album_components import AlbumControlPanel, AlbumUploadPhotoButton, ImageCard
from pages.page import Page


class AlbumPage(Page):

    @property
    def title(self) -> str:
        return self.control_panel.title

    @property
    def control_panel(self) -> AlbumControlPanel:
        return AlbumControlPanel(self.driver)

    @property
    def upload_photo_button(self) -> AlbumUploadPhotoButton:
        return AlbumUploadPhotoButton(self.driver)

    def delete_album(self) -> None:
        self.control_panel.delete_album()

    def upload_photo(self, path) -> ImageCard:
        return self.upload_photo_button.upload(path)
