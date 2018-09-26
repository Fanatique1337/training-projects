#!/usr/bin/env python3

"""A Postgresql benchmarking utility"""

import argparse
import os
import sys

import psycopg2
from timeit import timeit

def get_arguments():
    parser = argparse.ArgumentParser(description="Some description")
    parser.add_argument("benchmark_mode",
                        type=str,
                        help="One of connection, command")
    parser.add_argument("--sslmode",
                        type=str,
                        help="Choose an ssl mode for the connection.",
                        default="disable")
    parser.add_argument("-n",
                        "--tests",
                        type=int,
                        help="Amount of tests to run.",
                        default=10)

    return parser.parse_args()

def test_connection(ssl="disable"):
    connection = psycopg2.connect(
        dbname   = 'fanatique', 
        user     = 'fanatique', 
        password = '',
        #host     = "10.20.1.38",
        #sslmode  = ssl
    )

def main():
    args = get_arguments()

    result = timeit("test_connection(ssl='{}')".format(args.sslmode),
        setup  = "from __main__ import test_connection",
        number = args.tests)

    print("Total: {}".format(result))
    print("Average: {}".format(result/args.tests))

main()