#!/usr/bin/env python

def main():
    cSize1 = input("How many columns would you like the first matrix to have?: ")
    while not cSize1.isdigit() or cSize1 == 0:
        cSize1 = input("Please enter a correct number for the column count of matrix 1: ")

    rSize1 = input("How many rows would you like the first matrix to have?: ")
    while not rSize1.isdigit() or rSize1 == 0:
        rSize1 = input("Please enter a correct number for the row count of matrix 1: ")

    cSize1 = int(cSize1)
    rSize1 = int(rSize1)
    one = [[0 for el in range(cSize1)] for ele in range(rSize1)]

    cSize2 = input("How many columns would you like the second matrix to have?: ")
    while not cSize2.isdigit() or cSize2 == 0:
        cSize2 = input("Please enter a correct number for the column count of matrix 2: ")

    rSize2 = input("How many rows would you like the second matrix to have?: ")
    while not rSize2.isdigit() or rSize2 == 0:
        rSize2 = input("Please enter a correct number for the row count of matrix 2: ")

    cSize2 = int(cSize2)
    rSize2 = int(rSize2)
    two = [[0 for el2 in range(cSize2)] for ele2 in range(rSize2)]
    
    print("First matrix:")
    for r in range(rSize1):
        print(one[r])
    print("Second matrix:")
    for r2 in range(rSize2):
        print(two[r2])

    for row in range(rSize1):
        for column in range(cSize1):
            temp = input("Enter row {} column {} element of matrix 1: ".format(row+1, column+1))
            while not temp.isdigit():
                temp = input("Please enter a correct number for row {} column {} of matrix 1: ".format(row+1, column+1))

            temp = int(temp)
            one[row][column] = temp

    for row in range(rSize1):
        print(one[row])

    for row in range(rSize2):
        for  column in range(cSize2):
            temp = input("Enter row {} column {} element of matrix 2: ".format(row+1, column+1))
            while not temp.isdigit():
                temp = input("Please enter a correct number for row {} column {} of matrix 2: ".format(row+1, column+1))
        
            temp = int(temp)
            two[row][column] = temp

    for row in range(rSize2):
        print(two[row])

    choice = 0

    print("1. matrix1 + matrix2")
    print("2. matrix1 - matrix2")
    print("3. matrix2 - matrix1")
    if(cSize1 == rSize2):
        print("4. matrix1 x matrix2")
        print("5. matrix2 x matrix1")
    choice = input("Choose the operation (from 1 to 5): ")
    while int(choice) < 1 or int(choice) > 5 or not choice.isdigit():
        choice = input("Wrong input. Please choose a number from 1 to 5: ")

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
