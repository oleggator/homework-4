from pages.page import Page
from pages.settings_components import GeneralForm


class GeneralPage(Page):
    CHANGE_BUTTON = '//*[@id="showPageCategoriesSelectsId"]'

    @property
    def form(self):
        return GeneralForm(self.driver)

    def change_name_and_description(self, name, description):
        form = self.form
        form.name = name
        form.description = description
        form.save()
        return self

    def change_category_of_group(self, category: str, subcategory=None):
        self.driver.find_element_by_xpath(self.CHANGE_BUTTON).click()
        form = self.form
        form.category = category
        form.subcategory = subcategory
        form.save()
        return self
