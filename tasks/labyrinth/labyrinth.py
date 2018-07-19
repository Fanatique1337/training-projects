#!/usr/bin/env python3

matrix = [
[' ', ' ', ' ', '*', ' ', ' ', ' '],
['*', '*', ' ', '*', ' ', '*', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', '*', '*', '*', '*', '*', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', 'e']
]

rows = len(matrix)
cols = len(matrix[0])

for y in range(cols):
	for x in range(rows):
		if matrix[x][y] == ' ':
			matrix[x][y] = 0
		elif matrix[x][y] == '*':
			matrix[x][y] = 1
		elif matrix[x][y] == 'e':
			matrix[x][y] = 2

#for row in range(rows):
#	print(matrix[row])

def traverse(x, y):
    if matrix[x][y] == 2:
        #print('Finish is at {}, {}'.format(x, y))
        return True
    elif matrix[x][y] == 1:
        #print('There is a wall at {}, {}'.format(x, y))
        return False
    elif matrix[x][y] == 3:
        #print('Got through {}, {}'.format(x, y))
        return False
    
    #print('Going through {}, {}'.format(x, y))

    # mark as visited
    matrix[x][y] = 3

    # explore neighbors clockwise starting by the one on the right
    if ((x < len(matrix)-1 and traverse(x+1, y))
        or (y > 0 and traverse(x, y-1))
        or (x > 0 and traverse(x-1, y))
        or (y < len(matrix[x])-1 and traverse(x, y+1))):
        return True

    return False

traverse(0, 0)



#for r in range(rows):
#	print(matrix[r])

for y in range(cols):
	for x in range(rows):
		if matrix[x][y] == 0:
			matrix[x][y] = ' '
		elif matrix[x][y] == 1:
			matrix[x][y] = '*'
		elif matrix[x][y] == 2:
			matrix[x][y] = 'e'
		elif matrix[x][y] == 3:
			matrix[x][y] = 'o'

for row in range(rows):
	print(matrix[row])