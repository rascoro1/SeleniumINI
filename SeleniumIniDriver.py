import errors
import os
import ast
from ConfigParser import RawConfigParser
import Template
from multiprocessing import Process, Pool

def temp_to_orig_section(temp_sec):
    """
    Change a temp section into its original.
    If it is its original it will return what was given.
    :param temp_sec: temporary section created by 'create_temp_batch'
    :return: orig section
    """
    section = temp_sec
    if temp_sec.startswith(('1', '2', '3', '4', '5', '6', '7', '8', '9')) and '~|~' in temp_sec:
        # This is a temp section
        section = temp_sec.split('~|~', 1)[1]
    return section


def func_run_dynamic(input_file, dynamic_dic, exclude, pprint):
    """
    Execute one dynamic template

    :param input_file: (string) The template file name
    :param dynamic_dic: (dict) The dictionary of the dynamic variables
    :return:
    """
    new_template_filename = create_dynamic_template(input_file, dynamic_dic)
    t = Template.Template()
    t.file_path = new_template_filename
    t.load_sections()
    t.set_execute_order()
    t.start_driver()
    report = t.run()
    if pprint:
        t.pprint(exclude_none=exclude)
    return t


def create_dynamic_template(fname, dynamic_dic):
    """
    Create a dynamic template by filling in the dynamic variables

    :param fname: (string) The name of the dynamic template file
    :param dynamic_dic: (dict) A dictionary of dynamic variables
    :return:
    """
    # open the template and find lines with dynamic variables
    # Once variables are found replace them with the designated value
    f = open(fname, 'r')
    orig_lines = f.readlines()
    f.close()
    new_lines = []
    for line in orig_lines:
        new_line = line
        for key in dynamic_dic:
            if "<{}>".format(key) in line:
                new_line = line.replace("<{}>".format(key), dynamic_dic[key])
        new_lines.append(new_line)

    # Creating the new template file name
    new_fname = ""
    for key in dynamic_dic:
        new_fname += "{}-".format(str(dynamic_dic[key]).replace('/', '|'))

    new_fname += fname
    if os.path.isfile(new_fname):
        raise errors.DynamicTemplateAlreadyExistsException("Dynamic Template '{}' already exists.".format(new_fname),9053)
    else:
        # Creating the new template file with dynamic variables included
        f = open(new_fname, 'a')
        for line in new_lines:
            f.write(line)
        f.close()
        return new_fname

class SeleniumIniDriver():
    """
    The Driver to SeleniumINI
    Uses the template class to create and manage templates
    Also adds functionality for dynamic templates
    """
    def __init__(self):
        self.batch = False
        self.concurrent = False
        self.dynamic = False
        self.exclude = False
        self.input_file = False
        self.output_file = False
        self.pprint = False
        self.templates = []
        self.input_files = []
        self.temp_files = []
        self.keep_temps = False

    ##################################
    #        Check Methods             #
    ##################################

    def check_input_file(self):
        """
        Check if the input file was given, exists and is a ini file.
        :return: N/A
        """
        if self.input_file is False:
            raise errors.NoINITemplateGivenException("input-file argument cannot be empty.", 9011)

        if not os.path.isfile(self.input_file):
            raise errors.TemplateINIFileDoesNotExistException("input-file '{}' does not exist.".format(self.input_file), 9012)

        if not self.input_file.endswith(".ini"):
            raise errors.TemplateFileIsNotAnINIFileException("input-file '{}' is not an INI file.".format(self.input_file), 9013)

    def check_output_file(self):
        """
        Check if the output file exists and is a valid path.
        :return: N/A
        """
        if self.output_file is not False:
            if os.path.isfile(self.output_file):
                raise errors.OutputFileAlreadyExistsException("output-file '{}' already exists.".format(self.output_file), 9021)

            try:
                f = open(self.output_file, 'w')
            except OSError:
                raise errors.InvalidOutputFilePathException("output-file '{}' is not a valid path.".format(self.output_file), 9022)
            f.close()

    def check_batch(self):
        """
        Check if the batch file given follows the guidelines and all of the template files in the batch file actually exsist.
        This method also populate the self.input_files with dictionaries contains the template filename and attribute associated with it
        :return:
        """



        if self.batch is not False:
            if not os.path.isfile(self.input_file):
                raise errors.BatchFileDoesNotExistException("input-file for batch '{}' does not exist.".format(self.input_file), 9031)

            self.input_file = self.create_temp_batch(self.input_file)

            config = RawConfigParser()
            config.read(self.input_file)
            sections = config._sections

            for sec in sections:
                if not os.path.isfile(temp_to_orig_section(sec)):
                    raise errors.TemplateINIFileDoesNotExistException("input-file '{}' does not exist.".format(sec), 9032)

                if not sec.endswith(".ini"):
                    raise errors.TemplateFileIsNotAnINIFileException("input-file '{}' is not an INI file.".format(sec), 9033)

                res = {'fname': sec}
                for attr in sections[sec]:
                    res[attr] = sections[sec][attr]

                self.input_files.append(res)
            self.dynamic = True

    def check_concurrent(self):
        """
        Check if concurrent is enabled and if so make sure a batch file was given
        :return:
        """
        if self.concurrent is True:
            self.batch = True
            if self.batch is False:
                raise errors.NoBatchFileWithConcurrentEnabled("Cannot run concurrent without batch file given.", 9041)

    def check_dynamic_variables(self, template_fname, dynamic_dict):
        """
        Find the dynamic variables given to make sure they are in the template filename.
        If a dynamic variable was given but not in the template it will error out

        :param template_fname: (string) The filename of the template file
        :param dynamic_dict: (dict) A dictionary of the dynamic variables
        :return:
        """
        f = open(template_fname, 'r')
        lines = f.readlines()
        f.close()
        for key in dynamic_dict:
            found = False
            for line in lines:
                if "<{}>".format(key) in line:
                    found = True

            if not found:
                raise errors.DynamicVariableNotFoundInTemplateException("Dynamic variable '{}' cannot be found in template file '{}'".format(dynamic_dict[key], template_fname), 9052)

    def check_dynamic(self):
        """
        Checking if dynamic input is valid.
        :return:
        """
        if self.dynamic is not False:
            # Dynamic is only True if batch file is given
            if self.dynamic is True:
                for ini_file in self.input_files:
                    fname = temp_to_orig_section(ini_file['fname'])
                    ini_file.__delitem__('fname')
                    ini_file.__delitem__('__name__')
                    self.check_dynamic_variables(fname, ini_file)
                    ini_file['fname'] = fname
            # Dynamic is a string given by user
            else:
                try:
                    self.dynamic = ast.literal_eval(self.dynamic)
                except:
                    raise errors.InvalidDynamicInputStringException("Dynamic string '{}' is not in dictionary form".format(self.dynamic), 9051)

                self.check_dynamic_variables(self.input_file, self.dynamic)

    def check_args(self):
        """
        Check all of the arguments
        :return:
        """
        self.check_input_file()
        self.check_output_file()
        self.check_concurrent()
        self.check_batch()
        self.check_dynamic()

    ##################################
    #        Run Methods             #
    ##################################
    def run_concurrent(self):
        """Create worked os the run_dynamic method so they can run in parrell"""
        print "input_files: {}".format(self.input_files)
        p = Pool(4)
        args = []
        for ini_dict in self.input_files:
            fname = ini_dict['fname']
            ini_dict.__delitem__('fname')
            fname = temp_to_orig_section(fname)
            args.append((fname, ini_dict, self.exclude, self.pprint))
        results = []
        for arg in args:
            results.append(p.apply_async(func_run_dynamic, arg))
        p.close()
        p.join()
        templates = [r.get() for r in results]
        for t in templates:
            self.temp_files.append(t.file_path)
            self.templates.append(t)

    def run_batch(self):
        """
        Execute a batch amount of templates
        :return:
        """
        print "Input Files: {}".format(self.input_files)
        for ini_dict in self.input_files:
            fname = ini_dict['fname']
            ini_dict.__delitem__('fname')
            fname = temp_to_orig_section(fname)
            self.run_dynamic(fname, ini_dict)


    def run_dynamic(self, input_file, dynamic_dic):
        """
        Execute one dynamic template

        :param input_file: (string) The template file name
        :param dynamic_dic: (dict) The dictionary of the dynamic variables
        :return:
        """
        new_template_filename = self.create_dynamic_template(input_file, dynamic_dic)
        t = Template.Template()
        t.file_path = new_template_filename
        t.load_sections()
        t.set_execute_order()
        t.start_driver()
        report = t.run()
        if self.pprint:
            t.pprint(exclude_none=self.exclude)
        self.templates.append(t)

    def run_normal(self):
        """
        Execute one static template
        :return:
        """
        t = Template.Template()
        print "Input file: {}".format(self.input_file)
        t.file_path = self.input_file
        t.load_sections()
        t.set_execute_order()
        t.start_driver()
        report = t.run()
        if self.pprint:
            t.pprint(exclude_none=self.exclude)
        self.templates.append(t)

    def run(self):
        """
        Check the args and make sure to run the specific run method associated with the args given.
        :return:
        """
        self.check_args()

        # TODO: I need to add concurrent support and figure out what the batch file will look like
        # if self.concurrent is True:
        #     self

        if self.batch is True and self.concurrent is True:
            print "Running Concurrent"
            self.run_concurrent()
        elif self.batch is True:
            print "Running Batch"
            self.run_batch()
        elif self.dynamic is not False:
            print "Running Dynamic"
            print "Dynamic: {}".format(self.dynamic)
            self.run_dynamic(self.input_file, self.dynamic)
        elif self.input_file is not False:
            print "Running Normal"
            self.run_normal()

        print "OUTPUT FILE: {}".format(self.output_file)
        if self.output_file is not False:
            print "Writing Output File"
            self.write_output()

        if not self.keep_temps:
            self.delete_temp_files()

    ##################################
    #        MISC Methods            #
    ##################################

    def create_dynamic_template(self, fname, dynamic_dic):
        """
        Create a dynamic template by filling in the dynamic variables

        :param fname: (string) The name of the dynamic template file
        :param dynamic_dic: (dict) A dictionary of dynamic variables
        :return:
        """
        # open the template and find lines with dynamic variables
        # Once variables are found replace them with the designated value
        f = open(fname, 'r')
        orig_lines = f.readlines()
        f.close()
        new_lines = []
        for line in orig_lines:
            new_line = line
            for key in dynamic_dic:
                if "<{}>".format(key) in line:
                    new_line = line.replace("<{}>".format(key), dynamic_dic[key])
            new_lines.append(new_line)

        # Creating the new template file name
        new_fname = ""
        for key in dynamic_dic:
            new_fname += "{}-".format(str(dynamic_dic[key]).replace('/', '|'))

        new_fname += fname
        if os.path.isfile(new_fname):
            raise errors.DynamicTemplateAlreadyExistsException("Dynamic Template '{}' already exists.".format(new_fname), 9053)
        else:
            # Creating the new template file with dynamic variables included
            f = open(new_fname, 'a')
            for line in new_lines:
                f.write(line)
            f.close()
            self.temp_files.append(new_fname)

            return new_fname

    def write_output(self):
        """
        Write all the reports to an output file
        :return:
        """
        for t in self.templates:
            t.append_log_report(self.output_file, self.exclude)

    def create_temp_batch(self, fname):
        """
        Read files and get sections of INI file

        :param fname:
        :return:
        """
        new_fname = ""
        f = open(fname, 'r')
        lines = f.readlines()
        sections = []
        new_lines = []
        section = {}
        i = 0
        for line in lines:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                # This is a section
                line = line.lstrip('[').rstrip(']')
                # IS the section already in sections?
                if line in sections:
                    new_line = "[{}~|~{}]".format(i, line)
                    new_lines.append(new_line)
                else:  # If not then append
                    new_lines.append("[{}]".format(line))
                sections.append(line)
                i += 1
            else:
                new_lines.append(line)

        new_fname = "temp-{}".format(fname)
        # Write new tempate file
        f = open(new_fname, 'w')
        for line in new_lines:
            f.write(line + "\n")
        f.close()
        self.temp_files.append(new_fname)
        return new_fname

    def delete_temp_files(self):
        for temp_file in self.temp_files:
            os.remove(temp_file)


