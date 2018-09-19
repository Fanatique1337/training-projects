#!/bin/bash

/usr/bin/awk -F '"' '{if (NF == 7) {if (length($(NF-1)) > 2) print $(NF-1)}}' access.log | /usr/bin/cut -d ' ' -f1 | /usr/bin/sort -n | /usr/bin/uniq -c | /usr/bin/sort -nr