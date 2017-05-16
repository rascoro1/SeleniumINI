from ConfigParser import RawConfigParser
from selenium import webdriver
import time
from Section import Section
from bcolors import bcolors
import os
import errors
DRIVER_PATH = "/Users/copelanda1/PycharmProjects/ChangePassword/chromedriver"

class Template():
    """
    This class represents a template file.
    It is made up of sections from the section class.
    """
    def __init__(self):
        self.file_path = None
        self.driver = None
        self.exec_order = None
        self.report = None

    def set_execute_order(self):
        """
        get the order of sections to execute from the template file
        :return: A list of the commands to execute
        """
        order = []
        if os.path.isfile(self.file_path):
            f = open(self.file_path, 'r')
        else:
            raise errors.TemplatePathNotFoundException("The template path cannot be found. Specify the correct template.", 4)
        lines = f.readlines()

        for line in lines:
            # print "Line: {}".format(line)
            if line.startswith('[') and line.rstrip().endswith(']'):
                section_name = line.replace('[', '').replace(']', '').replace(' ', '').replace('\n', '')
                print "Found section: {}".format(section_name)
                if section_name != 'general':
                    order.append(section_name)

        f.close()
        # print "order: {}".format(order)
        self.exec_order = order

    def set_template_path(self, path):
        """
        Sets the template path self.file_path
        :param path: The path to the template file
        """
        self.file_path = path

    def start_driver(self):
        """
        This starts the webdriver and goes to the url specified in the template
        """
        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.driver.get(self.general.url)

    def stop_driver(self):
        """
        Stop and close the driver
        :return:
        """
        self.driver.quit()
        self.driver = None

    def load_sections(self):
        """
        This method will load all of the sections to the template.
        Each section will become its own attribute according to the template
        e.g. logon_username section will turn into t.logon_username which is type(t.logon_username) == Sections()
        """
        config = RawConfigParser()
        config.read(self.file_path)
        sections = config._sections

        for sec in sections:
            new_section = Section()
            new_section.set_name(sec)
            new_section.template = self
            for attr in sections[sec]:
                new_section.set_attribute(attr, sections[sec][attr])
            setattr(self, sec, new_section)

    def run(self):
        """
        This method is invoked when running on the template is ready.
        :return: The report of the run
        """
        print "Template dir: {}".format(dir(self))
        print "Execution Order: {}".format(self.exec_order)
        report = {}
        time.sleep(float(self.general.start_wait))
        for section in self.exec_order:
            print "Executing section: {}".format(section)
            sec = getattr(self, section)
            res = sec.execute()
            report[res['name']] = res
            time.sleep(float(self.general.between_wait))

        self.report = report

        print "Closing the Browser/Driver"
        self.stop_driver()

        return report

    def pprint(self, exclude_none=False):
        """
        pretty print the report with nice and preetttyyy collors
        """
        if self.report is None:
            print "No report to print please run the template"
        else:
            for section_name in self.exec_order:
                o_sec = getattr(self, section_name)
                o_sec.pprint(exclude_none=exclude_none)

    def append_log_report(self, log_fname, exclude):
        """
        Append the log report of all the sections of the template

        :param log_fname: (string) Name of the log file.
        :param exclude: (bool) (bool) Exclude section actions that were not performed/tried
        :return: Create a log report of this template
        """
        f = open(log_fname, 'a')
        f.write('~~########################~~\n')
        f.write(self.file_path + '\n')
        f.write('~~########################~~\n')
        f.close()
        for s in self.exec_order:
            s = getattr(self, s)
            s.append_log_report(log_fname, exclude)
