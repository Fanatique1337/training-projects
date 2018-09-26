#!/usr/bin/env python3

"""
A simple printing utility for brainbench tests.
Supply it with a file 'links.txt' containing an 
URL of the document you want to print on each new line.
Default file used is 'links.txt', can
be changed with the -f/--file argument.

VERSION: 1.3
"""

import argparse
import importlib
import os
import sys
import subprocess

import cups
import pdfkit

# # CONSTANTS # #

# Exit codes:
DEPENDANCY_ERROR = 4
ARGPARSE_ERROR   = 5
FILE_ERROR       = 6
DOWNLOAD_ERROR   = 7
IP_ERROR         = 8
CUPS_ERROR       = 9
GLOBAL_ERROR     = 10

# Maintainer constants:
DEBUG = False

# Program constants:
DEFAULT_SOURCE = "links.txt"

PDF_OPTIONS = {
    "dpi": "72",
    "grayscale": None,
    "page-size": "A4",
    "no-background": None,
    "disable-javascript": None
}

PRINT_OPTIONS = {
    "job-priority": "70",
    "fit-to-page": "",
    "media": "A4"
}

# Code:
def get_args():
    """
    Gets user-defined arguments.
    -f/--file is to specify an input file containing all the URLs.
    -p/--printer is to specify the name of the printer to send the
    documents to (as defined by CUPS).
    If no printer is specified by using -p/--printer, the default
    CUPS printer is used. Sends CUPS printing options specified
    in the PRINT_OPTIONS dictionary.
    """

    parser = argparse.ArgumentParser(description="Printing utility")
    parser.add_argument("-f",
                        "--file",
                        help="Specify the file to read the URLs from.",
                        type=str,
                        default=DEFAULT_SOURCE)
    parser.add_argument("-p",
                        "--printer",
                        help="Specify the name of the printer to print to.",
                        type=str,
                        default=None)
    return parser.parse_args()

def check_dependancies():
    """
    Check whether all dependancies are installed.
    This includes wkhtmltopdf linux utility, cups utility,
    and pdfkit module.
    To install wkhtmltopdf on Debian-based distros:
    sudo apt install wkhtmltopdf
    To install cups on Debian-based distros:
    sudo apt install cups
    To install pdfkit module:
    sudo apt install python3-pdfkit
    or if it isn't in the repos:
    sudo apt install python3-pip
    sudo pip3 install pdfkit

    If there are missing dependancies, the function
    will raise an OSError which will be caught in main().
    """
    missing = 0

    if subprocess.call('wkhtmltopdf > /dev/null 2>&1', shell=True) == 127:
        print("Missing dependancy: wkhtmltopdf is not installed.")
        missing += 1

    if subprocess.call('cupsctl > /dev/null 2>&1', shell=True) == 127:
        print("Missing dependancy: cupsctl is not installed.")
        missing += 1

    if importlib.util.find_spec("pdfkit") is None:
        print("Missing dependancy: pdfkit python module is not installed.")
        missing += 1

    if missing > 0:
        print("{} missing dependancies found. Aborting.", file=sys.stderr)
        raise OSError("Dependancies missing.")
    else:
        print("All dependancies found.")

def get_urls(source):
    """
    Opens the specified file and saves all the lines to a list.
    """

    with open(source, 'r', encoding="utf-8") as file:
        return file.readlines()

def download(links):
    """
    Downloads all documents from the specified URL
    and saves them as PDFs. Processes them by using
    PDF_OPTIONS.
    Now splits the link by using the query parameters
    and parses all of them, to make sure that the script
    won't break if brainbench added more query parameters.
    """

    downloaded = []
    params = {}

    for count, url in enumerate(links):
        queries = url.strip().split('?')[1:]
        for query in queries:
            query = query.split('=')
            params[query[0]] = query[1]

        output = '{}.pdf'.format(params["testid"])
        print("Downloading {} [{}/{}]...".format(output, count+1, len(links)))
        pdfkit.from_url(url, output, options=PDF_OPTIONS)
        print("Downloaded {}".format(output))
        downloaded.append(output)

    return downloaded

def send_print(pdfs, printer):
    """
    Sends all the documents to the CUPS Printer to print them.
    Raises CUPSError if no printer can be found.
    """

    #TODO: Error handling with assert, user/system error

    connection = cups.Connection()
    if printer:
        printers = connection.getPrinters()
        if printer not in printers:
            print("The printer {} cannot be found.", file=sys.stderr)
            print("List of available printers: {}".format(printers))
            sys.exit(CUPS_ERROR)
    elif not printer:
        printer = connection.getDefault()

    if printer:
        print("Sending files to printer...")
        jid = connection.printFiles(printer, pdfs, "Tests", PRINT_OPTIONS)
        print("Job sent successfuly.")
        print("Job ID: {}".format(jid))
        print("Job Priority: {}".format(PRINT_OPTIONS["job-priority"]))
    else:
        print("CUPS cannot find a default printer.", file=sys.stderr)
        sys.exit(CUPS_ERROR)

def main():
    """
    Handle errors and logic sequence.
    """
    try:
        check_dependancies()
    except OSError as dependancy_error:
        print(dependancy_error)
        sys.exit(DEPENDANCY_ERROR)

    try:
        args = get_args()
    except argparse.ArgumentError as argument_error:
        print("There was an error while handling your arguments.")
        print(argument_error)
        sys.exit(ARGPARSE_ERROR)

    try:
        links = get_urls(args.file)
    except PermissionError as permission_error:
        print("No permissions to open {}.".format(args.file))
        print(permission_error)
        sys.exit(FILE_ERROR)
    except FileNotFoundError as not_found_error:
        print("File {} cannot be found.".format(args.file))
        print(not_found_error)
        sys.exit(FILE_ERROR)

    try:
        pdfs = download(links)
    except OSError as wrong_url_error:
        print("A supplied URL is most likely wrong.")
        print(wrong_url_error)
        sys.exit(DOWNLOAD_ERROR)

    try:
        send_print(pdfs, args.printer)
    except cups.IPPError as cups_ip_error:
        print("There was a problem with the networking socket.")
        print(cups_ip_error)
        sys.exit(IP_ERROR)

if __name__ == "__main__":
    if DEBUG:
        main()
    else:
        try:
            main()
        except Exception as error:
            print("A global exception has been caught.")
            print(error)
            sys.exit(GLOBAL_ERROR)
