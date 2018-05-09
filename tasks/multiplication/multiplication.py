#!/usr/bin/env python

number = int(input("Enter a number: "))
if number <= 0 or number >= 3200000:
	print("Number must be between 0 and 3200000, try again.")
	while number <= 0 or number >= 3200000:
		number = int(input("Enter a number: "))

row = 0
counter = 1
rowlist = []
while counter <= number:
	row = counter ** 2
	tmp = str(row)
	for digit in tmp:
		rowlist.append(int(digit))
	counter += 1
			

print(rowlist[number-1])

