#!/usr/bin/env python3

string = 'a'
packetfile = 'packets.dat'

with open(packetfile, 'w+') as file:
    for x in range(28):
        file.write(string)
        file.write('\n')
        print("Written {} lines".format(x))
        string *= 2


