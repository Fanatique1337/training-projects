#!/usr/bin/env python3

AUTHENTICATION_FILE = 'auth.data'
MAX_TRIES = 3
LOGINS = 2

def load_authentication(config):

    with open(config, 'r') as auth_file:
        lines = auth_file.readlines()

    auth_database = {}
    for line in lines:
        line = line.split(',')
        auth_database[line[0]] = line[1]

    return auth_database

def main():

    users = load_authentication(AUTHENTICATION_FILE)

    used_usernames = []
    for login in range(LOGINS):

        success = False

        for tries in range(MAX_TRIES):
            username_attempt = input("Player {}'s username: ".format(login+1))
            password_attempt = input("Player {}'s password: ".format(login+1))

            if username_attempt in used_usernames:
                print("Please log in with another account.")
                print("You have {} tries left.".format(MAX_TRIES - tries+1))

            elif username_attempt in users:
                if password_attempt == users[username_attempt]:
                    print("Access authorised. Welcome, player {}".format(login+1))
                    used_usernames.append(username_attempt)
                    success = True
                    break

            else:
                print("Wrong username or password.")
                print("You have {} tries left.".format(MAX_TRIES - tries+1))

        if not success:
            print("Access denied.")

    if len(used_usernames) == LOGINS:
        print("All players have logged successfully.")


main()




