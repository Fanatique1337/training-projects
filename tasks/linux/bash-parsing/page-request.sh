#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Must provide the access log as an argument."
    exit 1
fi

if [ ! -e $1 ]; then
    echo "$1 does not exist."
    exit 1
fi

/usr/bin/awk '
{
    if (NF > 2 && length($(NF-2)) > 6) { 
            if ($(NF-2) > 5000000) 
                print $(NF-2),$8
    }
}' $1                                 | 
/usr/bin/awk '{if (NF > 1) print $2}' | 
/usr/bin/cut -d '?' -f1               |   
/usr/bin/sort -n                      | 
/usr/bin/uniq -c                      | 
/usr/bin/sort -nr                     ; 