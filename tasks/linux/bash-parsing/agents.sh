#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Must provide the access log as an argument."
    exit 1
fi

if [ ! -e $1 ]; then
    echo "$1 does not exist."
    exit 1
fi


/usr/bin/awk -F '"' '
{
    if (NF == 7) {
        if (length($(NF-1)) > 2) 
            print $(NF-1)
    }
}' $1                   | 
/usr/bin/cut -d ' ' -f1 | 
/usr/bin/sort -n        | 
/usr/bin/uniq -c        | 
/usr/bin/sort -nr       ;