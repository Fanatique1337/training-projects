#!/usr/bin/env python3

"""
A simple printing utility.
Supply it with a file 'links.txt'
containing an URL of the document
you want to print on each new line.
Default file used is 'links.txt', can
be changed with the -f/--file argument.
"""

import argparse
import importlib
import os
import sys
import subprocess

import cups
import pdfkit

# # CONSTANTS # #

# Error codes:
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
    "enable-javascript": None
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
    """

    parser = argparse.ArgumentParser(description="Printing utility",
                                     epilog="Needs 'links.txt' to work.")
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

def setup():
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
    """
    missing = 0

    if subprocess.call('wkhtmltopdf > /dev/null 2>&1', shell=True) == 127:
        print("Missing dependancy: wkhtmltopdf is not installed.")
        missing += 1

    if subprocess.call('cupsctl > /dev/null', shell=True) == 127:
        print("Missing dependancy: cupsctl is not installed.")
        missing += 1

    if importlib.util.find_spec("pdfkit") is None:
        print("Missing dependancy: pdfkit python module is not installed.")
        missing += 1

    if missing > 0:
        print("{} missing dependancies found. Aborting.", file=sys.stderr)
        sys.exit(DEPENDANCY_ERROR)
    else:
        print("All dependancies found.")

def get_urls(source):
    """
    Opens the specified file and saves all the lines to a list.
    """

    with open(source, 'r') as file:
        links = file.readlines()

    return links

def download(links):
    """
    Downloads all documents from the specified URL
    and saves them as PDFs. Processes them by using
    PDF_OPTIONS.
    """

    downloaded = []

    for url in links:
        if '=' in url:
            output = '{}.pdf'.format(url.strip().split('=')[1])
        else:
            output = '{}.pdf'.format(url.strip().split('/')[-1])
        count = links.index(url) + 1
        total = len(links)
        print("Downloading {} [{}/{}]...".format(output, count, total))
        pdfkit.from_url(url, output, options=PDF_OPTIONS)
        print("Downloaded {}".format(output))
        downloaded.append(output)

    return downloaded

def send_print(pdfs, printer):
    """
    Sends all the documents to the CUPS Printer to print them.
    If no printer is specified by using -p/--printer, the default
    CUPS printer is used. Sends CUPS printing options specified
    in the PRINT_OPTIONS dictionary.
    Raises CUPSError if no printer can be found.
    """

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

    setup()

    try:
        args = get_args()
    except argparse.ArgumentError as argerror:
        print("There was an error while handling your arguments.")
        print(argerror)
        sys.exit(ARGPARSE_ERROR)

    try:
        links = get_urls(args.file)
    except OSError as urlerror:
        print("No permissions or {} does not exist".format(args.file))
        print(urlerror)
        sys.exit(FILE_ERROR)

    try:
        pdfs = download(links)
    except OSError as downerror:
        print("A supplied URL is most likely wrong.")
        print(downerror)
        sys.exit(DOWNLOAD_ERROR)

    try:
        send_print(pdfs, args.printer)
    except cups.IPPError as cupserror:
        print("There was a problem with the networking socket.")
        print(cupserror)
        sys.exit(IP_ERROR)

if DEBUG:
    main()
else:
    try:
        main()
    except Exception as error:
        print("A global exception has been caught.")
        print(error)
        sys.exit(GLOBAL_ERROR)
