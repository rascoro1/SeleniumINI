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
## Using the SeleniumINI CLI
This was created to make running tests even easier than before.
With the SeleniumINI CLI we can run template files directly from the terminal.
Also I added functionality for dynamic templates, batch template exectuion and concurrent tests.

```
usage: SeleniumINICLI.py [-h] [-b] [-c] [-d DYNAMIC] [-e] [-i INPUT_FILE] [-k]
                         [-o OUTPUT_FILE] [-p]

optional arguments:
  -h, --help            show this help message and exit
  -b, --batch           Creating report from a batch amount of templates
  -c, --concurrent      Only used when the --batch flag has been used, speficy
                        the amount of concurrent browsers should be running at
                        once.
  -d DYNAMIC, --dynamic DYNAMIC
                        If you incorporated dynamic variables in you template
                        ini. Declare them here in a string in python diction
                        form. e.g. '{"url": "something.com"}'
  -e, --exclude         Will exclude element actions that were not performed.
  -i INPUT_FILE, --input-file INPUT_FILE
                        The file of the template file
  -k, --keep-temps      Keep temporary files that were created by
                        SeleniumINIDriver
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The report outputted to a file
  -p, --pprint          The report pretty printed to terminal

```
#### Running a Static Template
```
SeleniumINICLI.py -i my_github.ini
```
Excluding actions not performed, pretty printing and outputing log file
```
SeleniumINICLI.py -i my_github.ini --exclude -o output.log --pprint
```
#### Running Dynamic Template
Dynamic Templates are templates that were created however small changes may happen between templates.
Dynamic Templates are the same as Static Templates except they contain value holders in the ini file.
The value holders appear as <var_name> in the template file.
When running dynamic template make sure to specify the --dynamic flag and pass in the correct variables.
In this example my_github.ini contains two variables 'url' and 'user'. I filled in these place holders with 'google.com' and 'rascoro1'
```
SeleniumINICLI.py -i my_github.ini --dynamic "{'url': 'google.com', 'user':'rascoro1'}"
```
#### Running Batch
This will run one after another.
Templates can either be dynamic or static.

Take a look at the bithub_batch.ini file to create batch files.
```
SeleniumINICLI.py -i github_batch.ini --batch
```
#### Running Concurrent
Concurrent can only be run with a batch file
Templates can either be dynamic or static.
```
SeleniumINICLI.py -i github_batch.ini --concurrent

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
