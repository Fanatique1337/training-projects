#!/bin/bash -e

# ========[ CONFIGURATION ]======== #

ESXI=`/bin/cat /etc/esxi_host_addr`
DEST="[datastore1] /backup"
ESXI_USER=`/bin/cat /etc/esxi_host_auth | /bin/grep username | /usr/bin/awk -F '=' '{ print $2 }'`
PASSWORD=`/bin/cat /etc/esxi_host_auth | /bin/grep password | /usr/bin/awk -F '=' '{ print $2 }'`

# ========[      CODE     ]======== #

for vm in `cat vms`;
do
    /usr/bin/bazaarvcb backup -H "$ESXI" -u "$ESXI_USER" -p "$PASSWORD" "$vm" "$DEST" --consolidate
done
