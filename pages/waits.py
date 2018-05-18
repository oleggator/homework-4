from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from pages.page import Locator


class element_not_found(object):
    def __init__(self, selector, strategy):
        self.selector_script = strategy.format(selector)

    def __call__(self, driver):
        not_found: bool = driver.execute_script(self.selector_script)
        return not_found


class element_not_found_by_xpath(element_not_found):
    SELECTOR_SCRIPT = '''
            let node = document.evaluate("{}",document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            return node === null            
       '''

    def __init__(self, selector):
        super().__init__(selector, self.SELECTOR_SCRIPT)


class element_not_found_by_css_selector(element_not_found):
    SELECTOR_SCRIPT = '''
                let node = document.querySelector("{}");
                return node === null            
           '''

    def __init__(self, selector):
        super().__init__(selector, self.SELECTOR_SCRIPT)


def wait(driver, timeout=10):
    return WebDriverWait(driver, timeout)


class number_of_elements_located(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)
        if len(elements) == self.count:
            return elements
        return False


class web_element_locator(object):

    def __init__(self, locator: Locator, timeout: int = 10):
        self.locator = locator
        self.timeout = timeout

    def __call__(self, method):
        def wrapped_f(other, *args, **kwargs):
            wait(other.driver, self.timeout).until(
                expected_conditions.presence_of_all_elements_located(self.locator)
            )
            return method(other, *args, **kwargs)

        return wrapped_f
