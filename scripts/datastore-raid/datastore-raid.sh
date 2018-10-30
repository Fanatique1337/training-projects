#!/bin/bash -e

PART_ONE="/home"
PART_TWO="/"

MOUNT_ONE=$(df $PART_ONE | tail -n 1 | cut -d ' ' -f 1)

echo $MOUNT_ONE

MOUNT_TWO=$(df $PART_TWO | tail -n 1 | cut -d ' ' -f 1)

echo $MOUNT_TWO

if [ "$MOUNT_ONE" == "$MOUNT_TWO" ]; then
    echo 0
    exit 1
fi

DISK_ONE_FILENAME=$(/usr/share/tbmon2/bin/get_vsphereapi_data.pl --server `/bin/cat /etc/esxi_host_addr` --sessionfile /tmp/vsphereapi_session | grep 'Hard disk 2|VirtualDisk.VirtualDiskFlatVer2BackingInfo|backing.fileName:' | rev | cut -d ' ' -f 1 | rev)
DISK_TWO_FILENAME=$(/usr/share/tbmon2/bin/get_vsphereapi_data.pl --server `/bin/cat /etc/esxi_host_addr` --sessionfile /tmp/vsphereapi_session | grep 'Hard disk 3|VirtualDisk.VirtualDiskFlatVer2BackingInfo|backing.fileName:' | rev | cut -d ' ' -f 1 | rev)