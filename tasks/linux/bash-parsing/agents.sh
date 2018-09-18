#!/bin/bash

/usr/bin/awk -F '"' '{if (NF > 6) {if (length($(NF-1)) > 2) print $(NF-1)}}' access.log | /usr/bin/awk '{print $1}' | /usr/bin/sort -n | /usr/bin/uniq -c | /usr/bin/sort -nr