#!/usr/bin/env python3

import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

difficulty = input(bcolors.FAIL + "Please choose a difficulty (from 1 to 3): " + bcolors.ENDC)

while difficulty.isdigit() == False:
    difficulty = input("Please choose a correct number from 1 to 3: ")

if difficulty.isdigit() == True:
    while int(difficulty) < 1 or int(difficulty) > 3:
        difficulty = input("Choose a correct number from 1 to 3: ")

difficulty = int(difficulty)

if difficulty == 1:
    number = random.randint(1,25)
    maxnum = 25
    tries = 5

if difficulty == 2:
    number = random.randint(1,100)
    maxnum = 100
    tries = 6

if difficulty == 3:
    number = random.randint(1,500)
    maxnum = 500
    tries = 7

print("A random number from" + bcolors.FAIL + " 1 to {}".format(maxnum) + bcolors.ENDC + " has been chosen.")

guess = int(input(bcolors.BOLD + "What is your first guess, human?: " + bcolors.ENDC))

while guess != number and tries > 0:
    if guess < number:
        print(bcolors.HEADER + "Your guess" + bcolors.OKGREEN + " is lower " + bcolors.HEADER + "than the number you seek." + bcolors.ENDC)
        guess = 0
    if guess > number:
        print(bcolors.HEADER + "Your guess" + bcolors.OKGREEN + " is higher " + bcolors.HEADER + "than the number you seek." + bcolors.ENDC)
        guess = 0
    tries -= 1
    guess = int(input(bcolors.OKBLUE + "What is your guess? You have {} tries left: ".format(tries) + bcolors.ENDC))


if guess == number:
    print(bcolors.OKGREEN + "Congratulations, you won, because your guess was correct!" + bcolors.ENDC)
elif tries <= 0:
    print(bcolors.WARNING + "Aww, sorry, but you ran out of tries. Better luck next time." + bcolors.ENDC)

