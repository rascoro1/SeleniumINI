import Template

"""
There is two ways on using SeleniumINI.
Both involve creating a template.ini file which will need to be filled with a attr_xpath and an action.

Report Method: We could just run the template to get the results with the Template.run() method.
Control Method: Or we could create our own script as shown in this example using the element we specified in the template.

    Report Method:
        The report method is good for testing UI on webpages.
        For example the report method could perform a report every day with the new code.
        Color representation of pprint:
            Header:
                GREEN: Element was found.
                RED: Element was not found.
            Body:
                GREEN: Element action was successful.
                BLUE: Element action was not performed.
                RED: Element action was not successful.

    Control Method:
        The control method is good for scraping pages or creating more complex reports.
        Using this method you have complete control over each element.
            (When element is found/When the element action is performed/perform element methods not possible with report method)

        The methods that need to be performed are Template.load_section() and Template.start_driver()

        After this you can pick which element you would like to find first or mess with.
        This file is the example of the control method.
"""

########################################################
#                   Init the browser                   #
########################################################
t = Template.Template()
t.file_path = "my_github.ini"

# load the sections into the template
t.load_sections()
# This is setting the order according to the hometown.ini
# t.set_execute_order()
# start the webdriver
t.start_driver()


########################################################
# Represents the search_input section of the template  #
########################################################

res = t.search_input.execute()

if res['found'] is False:
    print "Element could not be found"
else:
    print "Element was found"
    if res['text'] is False:
        print "Could not find text for this element"
    elif res['text'] is None:
        print "Did not try to find element text"
    else:
        print "Found text for element: {} with value {}".format(t.search_input.name, res['text'])

    if res['send_keys'] is False:
        print "Could not send keys to this element"
    elif res['send_keys'] is None:
        print "Did not try to send keys to element"
    else:
        print "Sent keys to element successfully"

    if res['submit'] is False:
        print "Could not submit the element."
    elif res['submit'] is None:
        print "Did not try to submit the element"
    else:
        print "Successfully submited element"

    # Since we do know this element was found
    # We can now use the selenium Element object if we would like to
    e = t.search_input.element
    # Getting the outerHTML attribute of this element
    e.get_attribute('outerHTML')

    #Click the element 3 times because why not
    e.click()
    e.click()
    e.click()

########################################################
# Represents the my_github_link section of the template#
########################################################
res = t.my_github_link.execute()
if res['found'] is True:
    print "Element was found"
    if res['click'] is True:
        print "Element was successfully clicked"
    elif res['click'] is None:
        print "Did not try to click element"
    elif res['click'] is False:
        print "Could not click the element"


########################################################
# Represents the repo_button section of the template   #
########################################################
res = t.repo_button.execute()
if res['found'] is True:
    print "Element was found"
    if res['click'] is True:
        print "Element was successfully clicked"
    elif res['click'] is None:
        print "Did not try to click element"
    elif res['click'] is False:
        print "Could not click the element"

##############################################################
# Represents the selenium_ini_repo section of the template   #
##############################################################
# If i just wanted the element without the report
element = t.selenium_ini_repo.find_element()
if element is None:
    print "The element could not be found"
else:
    print "The element was found"

res = t.selenium_ini_repo.execute()

if res['found'] is True:
    print "Element was found"
    if res['click'] is True:
        print "Element was successfully clicked"
        print "We successfully reached our destination"
        print "Lets close the browser"
        t.stop_driver()
    elif res['click'] is None:
        print "Did not try to click element"
    elif res['click'] is False:
        print "Could not click the element"
