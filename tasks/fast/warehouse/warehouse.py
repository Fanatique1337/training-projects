#!/usr/bin/env python

size = 0
size = int(input("Enter the size of the warehouse's side in meters: "))
while size < 1 or size > 100:
	print("The size must be a number between 1 and 100 meters. Please enter the size again.")
	size = int(input("Enter the size of the warehouse's side in meters: "))

print(size)

storagemap = [] 
temp = []
counter = 0

while counter < size:
	temp = input("Enter the stock map for line {}: ".format(counter+1))
	temp = [words for segments in temp for words in segments.split()]
	storagemap.extend(temp)
	counter += 1

print(storagemap)

counter2 = 1
stocknum = 0
free = 0
freeway = 0
while counter2 < size ** 2 - size:
	if storagemap[counter2-1] == storagemap[counter2] and storagemap[counter2-1] == '1':
		print("Match")
		stocknum += 1

	if storagemap[counter2-1] == storagemap[counter2] and storagemap[counter2] == '0':
		free += 1
		if free >= size:
			freeway += 1
	if storagemap[counter2-1] == storagemap[counter2-1+size] and storagemap[counter2] == '0':
		free += 1
		if free >= size:
			freeway += 1
	counter2 += 1

print(freeway, free, stocknum)
	

