# SeleniumINI
Control a Selenium Driver using INI files.
![Demo](https://github.com/rascoro1/SeleniumINI/blob/master/demo.gif)

## Template File (.ini)
Each template file represents a flow within the browser.

### General
General section is where we can modify general attributes. <br />
Below are the currently supported attributes<br />
**url**:The url to the webpage<br />
**start_wait**: The time from start to first action<br />
**between_wait**: The time to wait before moving onto the next element/section<br />
**between_action_wait**: The time to wait before each action is preformed on a specific element/section<br />
<br />
```
Example
  url=https://www.google.com/
  start_wait=
  between_wait=1
  between_action_wait=.5
```

### Other Section
Each other section can have any type of name. <br />
For instance the submit button on a webpage could be the section: [submit_button]<br />
And the search text could be name: [search_input_text]<br />
Each one of these sections have specific attribute that are allowed.<br />
Below are the attribute that can be placed within these sections:<br />
**attr_xpath**: The xpath to the element you are looking for<br />
**send_keys**: The keys to be sent to this element<br />
**click**: Boolean either click or do not click element (True/False)<br />
**text**: If you would like to obtain the element type (True/False)<br />
**clear**: If you would like to clear the value in the text field (True/False)<br />
**submit**: Submit the form (True/False)<br />
**get_attribute**: Get a specific attribute from the selenium.Element e.g "outerHTML"<br />
**is_displayed**: Is the element displayed (True/False)<br />
**is_enabled**: Is the element enabled (True/False)<br />
**is_selected**: Is the element selected (True/False)<br />

```ini
Example:
  [general]
  url=https://www.google.com/
  start_wait=1
  between_wait=1
  between_action_wait=.5

  [search_input]
  attr_xpath=//div/input[contains(@title, "Search")]
  send_keys=rascoro1
  submit=True
```

## Implementing the Template with SeleniumINI
This is the easest part since creating the .ini is most of the work.<br />
Initilize the Template then point the template object to the ini file.<br />
Load the sections and set the execute order, This can be set by you if you would like to mess around with this.<br />
Start the driver and then run the driver.<br />
After a report will be returned as a dictionary.<br />
If you would like to show the report nicely and with color you can us pprint()<br />

```python
import Template

t = Template.Template()
# the template we are choosing
t.file_path = "my_github.ini"
# load the sections into the template
t.load_sections()
# This is setting the order according to the 'my_github.ini'
t.set_execute_order()
# start the webdriver
t.start_driver()
# run the scraper
report = t.run()
# Exclude attributes that have value None since they were not searched for
# And were not specificed in the template.
t.pprint(exclude_none=True)
```




