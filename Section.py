import errors

class Section():
    """
    This class represents the Sections that are in templates
    """
    VALID_ATTRIBUTES = [
        "attr_xpath",
        "url",
        "send_keys",
        "click",
        "text",
        "clear",
        "submit",
        "start_wait",
        "between_wait"
    ]

    def __init__(self):
        self.name = None
        self.template = None
        self.attr_xpath = False
        self.url = False
        self.text = False
        self.clear = False
        self.send_keys = False
        self.get_attribute = False
        self.is_displayed = False
        self.is_enabled = False
        self.is_selected = False
        self.submit = False
        self.click = False
        self.start_wait = 1
        self.between_wait = .5

    def set_attribute(self, attr, value):
        """
        Set an attribute for a section

        :param attr: The attribute name
        :param value: The value we are setting it to
        """
        if attr in Section.VALID_ATTRIBUTES:
            setattr(self, attr, value)
        else:
            # Skip the __name__ attribute
            if attr != "__name__":
                # Attribute is not a valid attribute
                raise errors.NotValidAttributeException("'{}' is an invalid attribute in the template file".format(attr), 1)

    def set_name(self, name):
        """
        Set the name of the section. self.name
        :param name: String: The name
        """
        self.name = name

    def execute(self):
        """
        Execute a specific section

        :return: exec_report which is a report of that specific execute
        """
        report = {
            'send_keys': None,
            'click': None,
            'name': self.name,
            'found': False,
            'text': None,
            'clear':None,
            'submit': None,
            'get_attribute':None,
            'is_displayed':None,
            'is_enabled':None,
            'is_selected':None
        }

        element = self.find_element()
        if element is not None:
            report['found'] = True

            if self.send_keys is not False:
                try:
                    element.send_keys(self.send_keys)
                    report['send_keys'] = True
                except:
                    report['send_keys'] = False

            if self.click is not False:
                try:
                    element.click()
                    report['click'] = True
                except:
                    report['click'] = False

            if self.text is not False:
                try:
                    str_text = element.text
                    report['text'] = str_text
                except:
                    report['text'] = False

            if self.clear is not False:
                try:
                    element.clear()
                    report['clear'] = True
                except:
                    report['clear'] = False

            if self.submit is not False:
                try:
                    element.submit()
                    report['submit'] = True
                except:
                    report['submit'] = False

            if self.get_attribute is not False:
                try:
                    res = element.get_attribute(self.get_attribute)
                    report['get_attribute'] = res
                except:
                    report['get_attribute'] = False

            if self.is_displayed is not False:
                try:
                    res = element.is_displated()
                    report['is_displayed'] = res
                except:
                    report['is_displayed'] = False

            if self.is_enabled is not False:
                try:
                    res = element.is_enabled()
                    report['is_enabled'] = res
                except:
                    report['is_enabled'] = False

            if self.is_selected is not False:
                try:
                    res = element.is_selected()
                    report['is_selected'] = res
                except:
                    report['is_selected'] = False

        return report

    def find_element(self):
        """
        Find an element on the webdriver page

        :return: element object or None if it is not found
        """
        try:
            element = self.template.driver.find_element_by_xpath(self.attr_xpath)
        except:
            element = None
        return element
