#!/usr/bin/env python3

"""
A simple printing utility.
Supply it with a file 'links.txt'
containing an URL of the document
you want to print on each new line.
Default file used is 'links.txt', can
be changed with the -f/--file argument.
"""

#TODO: wkhtmltopdf, pdfkit, cups

import argparse
import os
import sys

import cups
import pdfkit

# # CONSTANTS # #

# Error codes:
ARGPARSE_ERROR = 5
FILE_ERROR     = 6
DOWNLOAD_ERROR = 7
IP_ERROR       = 8
CUPS_ERROR     = 9
GLOBAL_ERROR   = 10

# Maintainer constants:
DEBUG = True

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
    args = parser.parse_args()

    return args

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
        print("Downloading {}...".format(output))
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
            print("The printer {} cannot be found.")
            print("List of available printers: {}".format(printers))
            sys.exit(1)
    elif not printer:
        printer = connection.getDefault()

    if printer:
        print("Sending files to printer...")
        jid = connection.printFiles(printer, pdfs, 'Tests', PRINT_OPTIONS)
        print("Job sent successfuly.")
        print("Job ID/Priority: {}/{}".format(jid, PRINT_OPTIONS["job-priority"]))
    else:
        print("CUPS cannot find a default printer.")
        sys.exit(CUPS_ERROR)

def main():
    try:
        args = get_args()
    except argparse.ArgumentError:
        print("There was an error while handling your arguments.")
        sys.exit(ARGPARSE_ERROR)

    try:
        links = get_urls(args.file)
    except OSError:
        print("No permissions or {} does not exist".format(args.file))
        sys.exit(FILE_ERROR)

    try:
        pdfs = download(links)
    except OSError:
        print("A supplied URL is most likely wrong.")
        sys.exit(DOWNLOAD_ERROR)

    try:
        send_print(pdfs, args.printer)
    except cups.IPPError:
        print("There was a problem with the networking socket.")
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
