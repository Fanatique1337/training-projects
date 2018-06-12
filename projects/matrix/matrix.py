#!/usr/bin/env python

"""Copyright 2018 Pavlin "Fanatique" Nikolov

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
limitations under the License."""

class bcolor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    cSize1 = input(bcolor.OKBLUE + "How many columns would you like the first matrix to have?: " + bcolor.ENDC)
    while not cSize1.isdigit() or cSize1 == 0:
        cSize1 = input(bcolor.FAIL + "Please enter a correct number for the column count of matrix 1: " + bcolor.ENDC)

    rSize1 = input(bcolor.OKBLUE + "How many rows would you like the first matrix to have?: " + bcolor.ENDC)
    while not rSize1.isdigit() or rSize1 == 0:
        rSize1 = input(bcolor.FAIL + "Please enter a correct number for the row count of matrix 1: " + bcolor.ENDC)

    cSize1 = int(cSize1)
    rSize1 = int(rSize1)
    one = [[0 for el in range(cSize1)] for ele in range(rSize1)]

    cSize2 = input(bcolor.OKBLUE + "How many columns would you like the second matrix to have?: " + bcolor.ENDC)
    while not cSize2.isdigit() or cSize2 == 0:
        cSize2 = input(bcolor.FAIL + "Please enter a correct number for the column count of matrix 2: " + bcolor.ENDC)

    rSize2 = input(bcolor.OKBLUE + "How many rows would you like the second matrix to have?: " + bcolor.ENDC)
    while not rSize2.isdigit() or rSize2 == 0:
        rSize2 = input(bcolor.FAIL + "Please enter a correct number for the row count of matrix 2: " + bcolor.ENDC)

    cSize2 = int(cSize2)
    rSize2 = int(rSize2)
    two = [[0 for el2 in range(cSize2)] for ele2 in range(rSize2)]
    
    print("\033[93mFirst matrix:\033[0m")
    for r in range(rSize1):
        print(one[r])
    print("\033[93mSecond matrix:\033[0m")
    for r2 in range(rSize2):
        print(two[r2])

    for row in range(rSize1):
        for column in range(cSize1):
            temp = input("\033[95mEnter \033[94mrow \033[92m{} \033[94mcolumn \033[92m{} \033[95melement of \033[94mmatrix \033[92m1: \033[0m".format(row+1, column+1))
            while not temp.isdigit():
                temp = input("\033[95mPlease enter a correct number for \033[94mrow \033[92m{} \033[94mcolumn \033[92m{} of \033[94m'matrix \033[92m1: \033[0m".format(row+1, column+1))

            temp = int(temp)
            one[row][column] = temp

    for row in range(rSize1):
        print(one[row])

    for row in range(rSize2):
        for  column in range(cSize2):
            temp = input("\033[95mEnter \033[94mrow \033[92m{} \033[94mcolumn \033[92m{} \033[95melement of \033[94mmatrix \033[92m2: \033[0m".format(row+1, column+1))
            while not temp.isdigit():
                temp = input("\033[95mPlease enter a correct number for \033[94mrow \033[92m{} \033[94mcolumn \033[92m{} of \033[94m'matrix \033[92m2: \033[0m".format(row+1, column+1))
        
            temp = int(temp)
            two[row][column] = temp

    for row in range(rSize2):
        print(two[row])

    choice = 0

    print("\033[93m1. Matrix #1 + Matrix #2")
    print("2. Matrix #1 - Matrix #2")
    print("3. Matrix #2 - Matrix #1")
    if(cSize1 == rSize2):
        print("4. Matrix #1 x Matrix #2")
        print("5. Matrix #2 x Matrix #1\033[0m")
    choice = input("\033[1mChoose the operation (from 1 to 5): \033[0m")
    while int(choice) < 1 or int(choice) > 5 or not choice.isdigit():
        choice = input("\033[91mWrong input. Please choose a number from 1 to 5: \033[0m")

    choice = int(choice)
    getchoice(choice, one, two, rSize1, rSize2, cSize1, cSize2)
    


def plus(a, b, rSize1, rSize2, cSize1, cSize2):
    print("plus")
    chckmaxrow = [rSize1, rSize2]
    chckmaxcol = [cSize1, cSize2]
    rSize3 = max(chckmaxrow)
    cSize3 = max(chckmaxcol)
    rSizemin = min(chckmaxrow)
    cSizemin = min(chckmaxcol)

    c = [[0 for el in range(cSize3)] for ele in range(rSize3)]
    for row in range(rSize1):
        for column in range(cSize1):
            c[row][column] = a[row][column]

    for row in range(rSize2):
        for column in range(cSize2):
            c[row][column] = b[row][column]

    for row in range(rSizemin):
        for column in range(cSizemin):
            c[row][column] = a[row][column] + b[row][column]

    for row in range(rSize3):
        print(c[row])

def minus(a, b, rSize1, rSize2, cSize1, cSize2):
    print("minus")
    chckmaxrow = [rSize1, rSize2]
    chckmaxcol = [cSize1, cSize2]
    rSize3 = max(chckmaxrow)
    cSize3 = max(chckmaxcol)
    rSizemin = min(chckmaxrow)
    cSizemin = min(chckmaxcol)

    c = [[0 for el in range(cSize3)] for ele in range(rSize3)]
    for row in range(rSize1):
        for column in range(cSize1):
            c[row][column] = a[row][column]

    for row in range(rSize2):
        for column in range(cSize2):
            c[row][column] = b[row][column]

    for row in range(rSizemin):
        for column in range(cSizemin):
            c[row][column] = a[row][column] - b[row][column]

    for row in range(rSize3):
        print(c[row])

def mult(a, b, rSize1, rSize2, cSize1, cSize2):
    print("mult")
    chckmaxrow = [rSize1, rSize2]
    chckmaxcol = [cSize1, cSize2]
    rSize3 = max(chckmaxrow)
    cSize3 = max(chckmaxcol)
    rSizemin = min(chckmaxrow)
    cSizemin = min(chckmaxcol)

    c = [[0 for el in range(cSize3)] for ele in range(rSize3)]

    if cSize1 == rSize2:
        for row in range(rSize1):
            for column in range(cSize1):
                c[row][column] = a[row][column]

        for row in range(rSize2):
            for column in range(cSize2):
                c[row][column] = b[row][column]

    if rSize3%2 == 0 and cSize3%2 == 0:
        for row in range(rSizemin):
            for column in range(cSizemin):
                if ((column+1)%2 == 0 and (row+1)%2 == 0) or row == rSize3 or column == cSize3:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column-1]*b[row-1][column]
                elif (column+1)%2 == 0 or column == cSize3:
                    c[row][column] = a[row][column]*b[row+1][column] + a[row][column-1]*b[row][column]
                elif (row+1)%2 == 0 or row == rSize3:
                    c[row][column] = a[row][column]*b[row-1][column] + a[row][column+1]*b[row][column]
                else:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column+1]*b[row+1][column]

    elif rSize3%2 == 1 and cSize3%2 == 1:
        for row in range(rSizemin):
            for column in range(cSizemin):
                if ((column+1)%2 == 1 and (row+1)%2 == 1) or row == rSize3 or column == cSize3:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column-1]*b[row-1][column]
                elif (column+1)%2 == 1 or column == cSize3:
                    c[row][column] = a[row][column]*b[row+1][column] + a[row][column-1]*b[row][column]
                elif (row+1)%2 == 1 or row == rSize3:
                    c[row][column] = a[row][column]*b[row-1][column] + a[row][column+1]*b[row][column]
                else:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column+1]*b[row+1][column]

    elif rSize3%2 == 1 and cSize3%2 == 0:
        for row in range(rSizemin):
            for column in range(cSizemin):
                if ((column+1)%2 == 0 and (row+1)%2 == 1) or row == rSize3 or column == cSize3:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column-1]*b[row-1][column]
                elif (column+1)%2 == 0 or column == cSize3:
                    c[row][column] = a[row][column]*b[row+1][column] + a[row][column-1]*b[row][column]
                elif (row+1)%2 == 1 or row == rSize3:
                    c[row][column] = a[row][column]*b[row-1][column] + a[row][column+1]*b[row][column]
                else:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column+1]*b[row+1][column]

    elif rSize3%2 == 0 and cSize3%2 == 1:
        for row in range(rSizemin):
            for column in range(cSizemin):
                if ((column+1)%2 == 1 and (row+1)%2 == 0) or (row == rSize3 and column == cSize3):
                    c[row][column] = a[row][column]*b[row][column] + a[row][column-1]*b[row-1][column]
                elif (column+1)%2 == 1 or column == cSize3:
                    c[row][column] = a[row][column]*b[row+1][column] + a[row][column-1]*b[row][column]
                elif (row+1)%2 == 0 or row == rSize3:
                    c[row][column] = a[row][column]*b[row-1][column] + a[row][column+1]*b[row][column]
                else:
                    c[row][column] = a[row][column]*b[row][column] + a[row][column+1]*b[row+1][column]



    for row in range(rSize3):
        print(c[row])

def getchoice(choice, one, two, r1, r2, c1, c2):
    if choice == 1:
        plus(one, two, r1, r2, c1, c2)

    if choice == 2:
        minus(one, two, r1, r2, c1, c2)

    if choice == 3:
        minus(two, one, r1, r2, c1, c2)

    if choice == 4:
        mult(one, two, r1, r2, c1, c2)

    if choice == 5:
        mult(two, one, r1, r2, c1, c2)



main()

"""
<> To do:
<1> Add comments for better understanding
<2> Add classes to use in other projects
<3> Complete the implementation and add new modes (normal use or implementation in other projects)
"""
