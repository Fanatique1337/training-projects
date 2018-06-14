#!/usr/bin/env python
import itertools


goatnum = 0
courses = 0
goatw = []
counter = 0
course = []

goatnum = int(input("Enter the number of goats: "))
courses = int(input("Enter the number of courses: "))
for g in range(goatnum):
	goatw.append(int(input("Enter the weight of goat #{}: ".format(g+1))))

goatw = sorted(goatw, reverse=True)
goatw1 = goatw[:len(goatw)/2]
goatw2 = goatw[len(goatw)/2:]
goats = sum(goatw)
result = []
while not result:
	result = [seq for i in range(len(goatw), 0, -1) for seq in itertools.permutations(goatw, i) if sum(seq) == int(sum(goatw)/2)]
	if not result:
		goats += 1
	else:
		break

print("Result: {}".format(result))
print(int(goats/2))

