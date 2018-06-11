#!/usr/bin/env python

numA = int(input("Type in a number A.\n"))
numB = int(input("Type in another number B.\n"))
string = input("Type in some text.\n")

print("This is A + B: {}".format(numA + numB))
print("This is A - B: {}".format(numA - numB))
print("This is A * B: {}".format(numA * numB))
print("This is A / B: {}".format(numA / numB))
print("This is A % B: {}".format(numA % numB))


print("This is the text you inputted with every word on a new line:")
string = string.split(' ')
for word in string:
	print(word)

