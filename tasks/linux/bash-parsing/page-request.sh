#!/bin/bash

/usr/bin/awk '{if (NF > 2 && length($(NF-2)) > 6) { if ($(NF-2) > 5000000) print $(NF-2),$8}}' access.log | /usr/bin/awk '{if (NF > 1) print $2}' | /usr/bin/cut -d '?' -f1 | /usr/bin/sort -n | /usr/bin/uniq -c | /usr/bin/sort -nr