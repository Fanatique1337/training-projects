#!/usr/bin/env python3

staticstring = 'b'
string = 'b'
packetfile = 'packets.dat'
start = 40950
up = 500

with open(packetfile, 'w+') as file:
    for x in range(50):
        file.write(string)
        file.write('\n')
        print("Written {} lines".format(x))
        string = string + staticstring * start
        start += up
        up = int(up * 1.2)


