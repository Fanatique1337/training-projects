#!/usr/bin/env python3
import sys

inp = input("").split(" ")
length = int(inp[0])
a = int(inp[1])
b = int(inp[2])
c = int(inp[3])
mx = 100000

if length > mx or a > mx or b > mx or c > mx:
	print("All numbers must be lower than 100 000.")
	sys.exit(3)

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

for dota in dots_a:
	for dotb in dots_b:
		tmp = max(dota, dotb)
		tmp2 = min(dota, dotb)
		if tmp - tmp2 == c:
			total += c

print(length-total)
print(dots_a)
print(dots_b)