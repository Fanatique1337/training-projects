#!/bin/bash

# BUFFERED (CACHE):

echo "Starting buffered sequential read..."
/usr/bin/fio --name=seqread --ioengine="libaio" --iodepth=1 --rw=read --direct=0 --bs=4k --size=16M --numjobs=4 --output=fio_nodirect_read
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=seqwrite --ioengine="libaio" --iodepth=1 --rw=write --direct=0 --bs=4k --size=16M --numjobs=4  --output=fio_nodirect_write
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=randread --ioengine="libaio" --iodepth=1 --rw=randread --direct=0 --bs=4k --size=16M --numjobs=4  --output=fio_nodirect_randread
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=randwrite --ioengine="libaio" --iodepth=1 --rw=randwrite --direct=0 --bs=4k --size=16M --numjobs=4  --output=fio_nodirect_randwrite

# DIRECT (NO CACHE):
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=directread --ioengine="libaio" --iodepth=1 --rw=read --direct=1 --bs=4k --size=16M --numjobs=4  --output=fio_direct_read
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=directwrite --ioengine="libaio" --iodepth=1 --rw=write --direct=1 --bs=4k --size=16M --numjobs=4  --output=fio_direct_write
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=directrandread --ioengine="libaio" --iodepth=1 --rw=randread --direct=1 --bs=4k --size=16M --numjobs=4  --output=fio_direct_randread
echo "Done"
echo "Starting next test..."
/usr/bin/fio --name=directrandwrite --ioengine="libaio" --iodepth=1 --rw=randwrite --direct=1 --bs=4k --size=16M --numjobs=4  --output=fio_direct_randwrite


