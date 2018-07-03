#!/usr/bin/env python3

inp = input("").split(" ")
length = int(inp[0])
a = int(inp[1])
b = int(inp[2])
c = int(inp[3])
#print(inp, length, a, b, c)

counter_a = 0
counter_b = length
dots_a = []
dots_b = []
total = 0

while(counter_a <= length):
	dots_a.append(counter_a)
	counter_a += a

while(counter_b >= 0):
	dots_b.append(counter_b)
	counter_b -= b

#print("A: {}".format(dots_a))
#print("B: {}".format(dots_b))

for dota in dots_a:
	for dotb in dots_b:
		tmp = max(dota, dotb)
		tmp2 = min(dota, dotb)
		if tmp - tmp2 == 1:
			total += 1

print(length-total)
