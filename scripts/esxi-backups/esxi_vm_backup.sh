#!/bin/bash -e

# ========[ CONFIGURATION ]======== #

ESXI=`/bin/cat /etc/esxi_host_addr`
DEST=`/bin/cat /etc/esxi_vm_backup | /bin/grep destination | /usr/bin/awk -F '=' '{print $2}'`
ESXI_USER=`/bin/cat /etc/esxi_host_auth | /bin/grep username | /usr/bin/awk -F '=' '{ print $2 }'`
PASSWORD=`/bin/cat /etc/esxi_host_auth | /bin/grep password | /usr/bin/awk -F '=' '{ print $2 }'`

# ========[      CODE     ]======== #

for VM in `/bin/cat /etc/esxi_vm_backup | /bin/grep vmname | /usr/bin/awk -F '=' '{print $2}'`;
do
    /usr/bin/bazaarvcb backup --consolidate -H "${ESXI}" -u "${ESXI_USER}" -p "${PASSWORD}" ${VM} "${DEST}"
    #/usr/bin/bazaarvcb backup --consolidate -H `printf "${ESXI}"` -u `printf "${ESXI_USER}"` -p `printf "${PASSWORD}"` `printf "${VM}"` `printf "${DEST}"`
done
