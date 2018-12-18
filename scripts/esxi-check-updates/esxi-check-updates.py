#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

# Define constants:

SUBPROCESS_ERROR = 4
ASSERT_ERROR     = 5
GLOBAL_ERROR     = 6

ESXI_DEPOT  = "https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml"
VIBS_SLICE  = 1 # This is the part of the split list where the VIB names are.
DEBUG_TRACE = False

def get_args():
    """
    Get the arguments for the script.
    -p/--profile should be the newest profile from https://esxi-patches.v-front.de/ESXi-6.0.0.html;
    -d/--depot should be the depot/repo to download the update from;
    --host should be the IP address or domain name of the ESXi host on which to test the update;
    -u/--username is the username used for SSH authentication.
    """

    parser = argparse.ArgumentParser(description="Check VMware ESXI version")

    parser.add_argument("-p",
                        "--profile",
                        type=str,
                        help="The newest ESXi profile.")
    parser.add_argument("-d",
                        "--depot",
                        type=str,
                        help="The depot/repo to update from.",
                        default=ESXI_DEPOT)
    parser.add_argument("--host",
                        type=str,
                        help="The IP or domain name of the ESXi host.")
    parser.add_argument("-u",
                        "--username",
                        type=str,
                        help="Username for the SSH connection to ESXi.")

    return parser.parse_args()

def main():

    args = get_args()

    assert isinstance(args, argparse.Namespace), "Internal error: args is not an argparse Namespace"

    command = "esxcli software profile update -p {} -d {} --dry-run --force".format(
        args.profile,
        args.depot
    )

    output = subprocess.check_output(['ssh {}@{} "{}"'.format(
        args.username,
        args.host,
        command)], shell=True)

    # Decode the output because check_output returns it in a bytes-like object.
    output = output.decode('utf-8').split('\n')

    # Get the info we need from the output.
    for line in output:
        if "vibs installed" in line.lower():
            vibs_installed = line.strip().split(':')[VIBS_SLICE] # VIBs installed
        if "vibs removed" in line.lower():
            vibs_removed = line.strip().split(':')[VIBS_SLICE] # VIBs removed
        if "vibs skipped" in line.lower(): 
            vibs_skipped = line.strip().split(':')[VIBS_SLICE] # VIBs skipped

    vibs_installed_count = vibs_installed.count(',')
    vibs_removed_count   = vibs_removed.count(',')
    vibs_skipped_count   = vibs_skipped.count(',')

    if vibs_installed_count == 0:
        vibs_installed = "N/A"
    if vibs_removed_count == 0:
        vibs_removed = "N/A"
    if vibs_skipped_count == 0:
        vibs_skipped = "N/A"

    print("VIBs installed count:{}".format(vibs_installed_count))
    print("VIBs installed:{}".format(vibs_installed))
    print("VIBs removed count:{}".format(vibs_removed_count))
    print("VIBs removed:{}".format(vibs_removed))
    print("VIBs skipped count:{}".format(vibs_skipped_count))
    print("VIBs skipped:{}".format(vibs_skipped))

if __name__ == "__main__":
    if not DEBUG_TRACE:
        try:
            main()
        except subprocess.CalledProcessError as err:
            print("Error: the ssh command exited with non-zero status.")
            print(err)
            sys.exit(SUBPROCESS_ERROR)
        except AssertionError as err:
            print("Assertion error caught:")
            print(err)
            sys.exit(ASSERT_ERROR)
        except Exception as err:
            print("Error: A global exception has been caught.")
            print(err)
            sys.exit(GLOBAL_ERROR)
    else:
        main()