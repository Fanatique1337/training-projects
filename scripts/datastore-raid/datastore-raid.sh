#!/bin/bash -e

PART_ONE="/home"
PART_TWO="/"

MOUNT_ONE=$(df $PART_ONE | tail -n 1 | cut -d ' ' -f 1)

echo ${MOUNT_ONE}

MOUNT_TWO=$(df $PART_TWO | tail -n 1 | cut -d ' ' -f 1)

echo ${MOUNT_TWO}

DISK_ONE_FILENAME=$(/usr/share/tbmon2/bin/get_vsphereapi_data.pl --server `/bin/cat /etc/esxi_host_addr` --sessionfile /tmp/vsphereapi_session | grep 'Hard disk 2|VirtualDisk.VirtualDiskFlatVer2BackingInfo|backing.fileName:' | rev | cut -d ':' -f 1 | rev)
DISK_TWO_FILENAME=$(/usr/share/tbmon2/bin/get_vsphereapi_data.pl --server `/bin/cat /etc/esxi_host_addr` --sessionfile /tmp/vsphereapi_session | grep 'Hard disk 3|VirtualDisk.VirtualDiskFlatVer2BackingInfo|backing.fileName:' | rev | cut -d ':' -f 1 | rev)
DISK_ONE_DATASTORE=$(echo ${DISK_ONE_FILENAME} | cut -d ' ' -f1 | cut -d '[' -f2 | cut -d ']' -f1)
DISK_TWO_DATASTORE=$(echo ${DISK_TWO_FILENAME} | cut -d ' ' -f1 | cut -d '[' -f2 | cut -d ']' -f1)

echo ${DISK_ONE_FILENAME}
echo ${DISK_TWO_FILENAME}
echo ${DISK_ONE_DATASTORE}
echo ${DISK_TWO_DATASTORE}

DISK_ONE_DATASTORE_EXTENT=$(/bin/esxcli storage vmfs extent list | grep ${DISK_ONE_DATASTORE} | awk '{print $4}')
DISK_TWO_DATASTORE_EXTENT=$(/bin/esxcli storage vmfs extent list | grep ${DISK_TWO_DATASTORE} | awk '{print $4}')

echo ${DISK_ONE_DATASTORE_EXTENT}
echo ${DISK_TWO_DATASTORE_EXTENT}

DISK_ONE_RAID_LEVEL=$(/bin/esxcli storage core device list -d ${DISK_ONE_DATASTORE_EXTENT} | grep "RAID Level: " | rev | cut -d ' ' -f1 | rev)
DISK_TWO_RAID_LEVEL=$(/bin/esxcli storage core device list -d ${DISK_TWO_DATASTORE_EXTENT} | grep "RAID Level: " | rev | cut -d ' ' -f1 | rev)

if [ "${MOUNT_ONE}" == "${MOUNT_TWO}" ]; then
    echo 0
    exit 1
fi

if [ "${DISK_ONE_DATASTORE}" == "${DISK_TWO_DATASTORE}" ]; then
    echo 0
    exit 1
fi

if [ "${DISK_ONE_DATASTORE_EXTENT}" == "${DISK_TWO_DATASTORE_EXTENT}" ]; then
    echo 0
    exit 1
fi

if [ "${DISK_ONE_RAID_LEVEL}" == "unknown" ]; then
    echo 0
    exit 1
fi

if [ "${DISK_TWO_RAID_LEVEL}" == "unknown" ]; then
    echo 0
    exit 1
fi

еcho 1
exit 0