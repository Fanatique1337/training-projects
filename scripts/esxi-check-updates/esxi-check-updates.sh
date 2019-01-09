#!/bin/bash -е

if [[ $# -eq 0 ]]; then
    echo "No arguments supplied. At least one argument (the newest profile) must be supplied."
    exit 1
fi

if [[ -z "$1" ]]; then
    echo "Missing argument: one argument must be supplied - newest profile name."
    exit 1
fi

PROFILE=$1

if [[ ! -z "$2" ]]; then
    DEPOT=$2
else
    DEPOT="https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml"
fi

/usr/bin/timeout 30 /usr/share/tbmon2/bin/esxi-check-updates.py -p ${PROFILE} -d ${DEPOT} \
--host `/bin/cat /etc/esxi_host_addr` --user `/bin/cat /etc/esxi_host_auth | /bin/grep username | /bin/cut -d '=' -f2`
