#!/usr/bin/env python

temp = input("First line: K rows, L columns and R days\n")
temp = temp.split()
temp[0] = int(temp[0])
temp[1] = int(temp[1])
temp[2] = int(temp[2])

if temp[0] <= 0 or temp[0] > temp[1] or temp[0] > 1000 or temp[1] <= 0 or temp[1] > 1000 or temp[2] <= 0 or temp[2] > 100:
	while temp[0] <= 0 or temp[0] > temp[1] or temp[0] > 1000 or temp[1] <= 0 or temp[1] > 1000 or temp[2] <= 0 or temp[2] > 100:
		temp = input("Requirements: 0 < K <= L <= 1000 and 0 < R <= 100. Try again. K rows, L columns and R days\n")
		temp = temp.split()
		temp[0] = int(temp[0])
		temp[1] = int(temp[1])
		temp[2] = int(temp[2])

rows = int(temp[0])
columns = int(temp[1])
days = int(temp[2])

straw1 = [0, 0]
straw2 = [0, 0]

straw1 = input("Position of the first strawberry: K row and L column\n").split()
straw1[0] = int(straw1[0])
straw1[1] = int(straw1[0])

if straw1[0] < 0 or straw1[0] > rows or straw1[1] < 0 or straw1[1] > columns:
	while straw1[0] < 0 or straw1[0] > rows or straw1[1] < 0 or straw1[1] > columns:
		straw1 = input("The position was not in the allowed range for the 1st strawberry. Try again, K row and L column\n").split()
		straw1[0] = int(straw1[0])
		straw1[1] = int(straw1[0])

straw2 = input("Position of the second strawberry: K row and L column\n").split()
straw2[0] = int(straw2[0])
straw2[1] = int(straw2[1])

if straw2[0] < 0 or straw2[0] > rows or straw2[1] < 0 or straw2[1] > columns:
	while straw2[0] < 0 or straw2[0] > rows or straw2[1] < 0 or straw2[1] > columns:
		straw2 = input("The position was not in the allowed range for the 2nd strawberry. Try again, K row and L column\n").split()
		straw2[0] = int(straw2[0])
		straw2[1] = int(straw2[1])

row1 = straw1[0]-1
col1 = straw1[1]-1
row2 = straw2[0]-1
col2 = straw2[1]-1

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

