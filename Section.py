import errors
import time

def str_to_boolean(string):
    """
    If the string is "True" or "False" it wil convert it to a Boolean type
    Else it return what was given to it.

    :param string: A input string
    :return:IF that string is "True" or "False" Then return the boolean otherwise return the result.
    """
    if string == "True":
        # print "True Found"
        string = True
    elif string == "False":
        # print "False Found"
        string = False
    return string

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
        "get_attribute",
        "is_displayed",
        "is_enabled",
        "is_selected",
        "start_wait",
        "between_wait",
        "between_action_wait"
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
        self.between_action_wait = .5

    def set_attribute(self, attr, value):
        """
        Set an attribute for a section

        :param attr: The attribute name
        :param value: The value we are setting it to
        """
        if attr in Section.VALID_ATTRIBUTES:
            setattr(self, attr, str_to_boolean(value))
        else:
            # Skip the __name__ attribute
            if attr != "__name__":
                # Attribute is not a valid attribute
                raise errors.NotValidAttributeException("'{}' is an invalid attribute in the template file {}".format(attr, self.template.file_path), 1)

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
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    element.send_keys(self.send_keys)
                    report['send_keys'] = True
                except:
                    report['send_keys'] = False

            if self.click is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    element.click()
                    report['click'] = True
                except:
                    report['click'] = False

            if self.text is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    str_text = element.text
                    report['text'] = str_text
                except:
                    report['text'] = False

            if self.clear is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    element.clear()
                    report['clear'] = True
                except:
                    report['clear'] = False

            if self.submit is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    element.submit()
                    report['submit'] = True
                except:
                    report['submit'] = False

            if self.get_attribute is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    res = element.get_attribute(self.get_attribute)
                    report['get_attribute'] = res
                except:
                    report['get_attribute'] = False

            if self.is_displayed is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    res = element.is_displated()
                    report['is_displayed'] = res
                except:
                    report['is_displayed'] = False

            if self.is_enabled is not False:
                time.sleep(float(self.template.general.between_action_wait))
                try:
                    res = element.is_enabled()
                    report['is_enabled'] = res
                except:
                    report['is_enabled'] = False

            if self.is_selected is not False:
                time.sleep(float(self.template.general.between_action_wait))
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
