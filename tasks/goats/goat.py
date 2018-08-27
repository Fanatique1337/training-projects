#!/usr/bin/env python
import itertools
from PIL import ImageDraw

goatnum = 0
courses = 0
goatw = []
counter = 0

goatnum = int(input("Enter the number of goats: "))
courses = int(input("Enter the number of courses: "))
for g in range(goatnum):
	goatw.append(int(input("Enter the weight of goat #{}: ".format(g+1))))

goatw = sorted(goatw, reverse=True)
goats = sum(goatw)
result = []
permlen = len(goatw)/courses
while not result:
	result = [seq for i in range(len(goatw), 0, -1) for seq in itertools.permutations(goatw, permlen) if sum(seq) == int(goats/courses)]
	if not result:
		goats += 1
		permlen += 1
	else:
		break

print(result)

