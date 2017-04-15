import Template

t = Template.Template()
# the template we are choosing
t.file_path = "hometown.ini"
# load the sections into the template
t.load_sections()
# This is setting the order according to the hometown.ini
t.set_execute_order()
# start the webdriver
t.start_driver()
# run the scraper
report = t.run()
t.pprint()
# Exclude attributes that have value None since they were not searched for
# And were not specificed in the template.
t.pprint(exclude_none=True)