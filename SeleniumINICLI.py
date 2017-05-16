#!/usr/bin/python3

"""
Run SeleniumINI in the terminal
"""

import SeleniumIniDriver
import argparse
import errors
from bcolors import bcolors

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--batch', action='store_true',
                        help='Creating report from a batch amount of templates', default=False)

    parser.add_argument('-c', '--concurrent', action='store_true',
                        help='Only used when the --batch flag has been used, speficy the amount of concurrent browsers should be running at once.', default=False)

    parser.add_argument('-d', '--dynamic', type=str,
                        help='If you incorporated dynamic variables in you template ini. Declare them here in a string in python diction form. e.g. \'{"url": "something.com"}\'', default=False)

    parser.add_argument('-e', '--exclude', action='store_true',
                        help='Will exclude element actions that were not performed.', default=False)

    parser.add_argument('-i', '--input-file', type=str,
                        help='The file of the template file', default=False)

    parser.add_argument('-k', '--keep-temps', action='store_true',
                        help='Keep temporary files that were created by SeleniumINIDriver', default=False)

    parser.add_argument('-o', '--output-file', type=str,
                        help='The report outputted to a file', default=False)

    parser.add_argument('-p', '--pprint', action='store_true',
                        help='The report pretty printed to terminal', default=False)


    args = parser.parse_args()

    sid = SeleniumIniDriver.SeleniumIniDriver()
    sid.batch = args.batch
    sid.concurrent = args.concurrent
    sid.dynamic = args.dynamic
    sid.exclude = args.exclude
    sid.input_file = args.input_file
    sid.keep_temps = args.keep_temps
    sid.output_file = args.output_file
    sid.pprint = args.pprint

    err_header = bcolors.FAIL + "ERROR: " + bcolors.ENDC

    try:
        sid.run()
    except errors.BatchFileDoesNotExistException as e:
        print "{}{}".format(err_header, e.message)
    except errors.DynamicVariableNotFoundInTemplateException as e:
        print "{}{}".format(err_header, e.message)
    except errors.ElementCannotBeFoundException as e:
        print "{}{}".format(err_header, e.message)
    except errors.InvalidDynamicInputStringException as e:
        print "{}{}".format(err_header, e.message)
    except errors.InvalidOutputFilePathException as e:
        print "{}{}".format(err_header, e.message)
    except errors.NoBatchFileWithConcurrentEnabled as e:
        print "{}{}".format(err_header, e.message)
    except errors.NoINITemplateGivenException as e:
        print "{}{}".format(err_header, e.message)
    except errors.NoReportFoundException as e:
        print "{}{}".format(err_header, e.message)
    except errors.NotValidAttributeException as e:
        print "{}{}".format(err_header, e.message)
    except errors.OutputFileAlreadyExistsException as e:
        print "{}{}".format(err_header, e.message)
    except errors.TemplateFileIsNotAnINIFileException as e:
        print "{}{}".format(err_header, e.message)
    except errors.TemplateINIFileDoesNotExistException as e:
        print "{}{}".format(err_header, e.message)
    except errors.TemplatePathNotFoundException as e:
        print "{}{}".format(err_header, e.message)
    except errors.DynamicTemplateAlreadyExistsException as e:
        print "{}{}".format(err_header, e.message)