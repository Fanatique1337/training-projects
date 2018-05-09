#!/usr/bin/env python

temp = input("First line: K rows, L columns and R days\n")
temp = temp.split()

rows = int(temp[0])
columns = int(temp[1])
days = int(temp[2])

straw1 = [0, 0]
straw2 = [0, 0]

straw1 = input("Position of the first strawberry: K row and L column\n").split()
straw2 = input("Position of the second strawberry: K row and L column\n").split()

row1 = int(straw1[0])-1
col1 = int(straw1[1])-1
row2 = int(straw2[0])-1
col2 = int(straw2[1])-1

map = [[0 for x in range(columns)] for y in range(rows)]
map[row1][col1] = 1
map[row2][col2] = 1

infected = []

counter = 1
counter2 = 0
c = 0

def infect(x, y):
	if x < rows-1:
		if map[x+1][y] == 0:
			map[x+1][y] = 1
	if x > 0:
		if map[x-1][y] == 0:
			map[x-1][y] = 1
	if y < columns-1:
		if map[x][y+1] == 0:
			map[x][y+1] = 1
	if y > 0:
		if map[x][y-1] == 0:
			map[x][y-1] = 1

while counter <= days:
	for rw in range(rows):
		for cl in range(columns):
			if map[rw][cl] == 1:
				infected.append(rw)
				infected.append(cl)
	length = len(infected)
	while counter2 < length/2:
		infect(infected[c], infected[c+1])
		c += 2
		counter2 += 1
	counter += 1

i = 0
for r in range(rows):
	for c in range(columns):
		if map[r][c] == 0:
			i += 1

#for r in range(rows):
#	print(map[r])

print(i)

