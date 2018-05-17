class element_not_found(object):
    def __init__(self, selector, strategy):
        self.selector_script = strategy.format(selector)

    def __call__(self, driver):
        not_found: bool = driver.execute_script(self.selector_script)
        return not_found

class element_not_found_by_xpath(element_not_found):
    SELECTOR_SCRIPT = '''
            let node = document.evaluate("{}",document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null ).singleNodeValue;
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
