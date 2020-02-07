from urllib.request import urlopen
from datetime import datetime
import os
import sys
import time
import control

def have_internet():
    try:
        urlopen("http://www.google.com", timeout=10)
        return True
    except:
        print('No access to internet')
        return False


def print_to_file():
    old_f = sys.stdout

    class F:
        def write(self, x):
            if (str(x) != "\n"):
                old_f.write("[" + str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + "]: " + str(x))
                old_f.flush()
            else:
                old_f.write(x)

        def flush(self):
            old_f.flush()

    sys.stdout = F()


def block_until_internet():
    print("The control system was started!")

    if not have_internet():
        print("Waiting until there is an internet connection to continue")
        while not have_internet():
            print("The device does not have internet")
            time.sleep(1)

    print("It was connected to internet!")


def internet_checker_thread():
    print("[New Thread]: The thread that verifies the internet connection was started")
    while True:
        if have_internet():
            # if I have a connection I can wait about 5 mins
            time.sleep(60 * 5)
        else:
            print("It was detected that there is no internet connection.")
        time.sleep(60)


def block_start_command_line(arguments):
    arguments.insert(0, "quit")
    time.sleep(0.5)
    print('Enter a command(' + ", ".join(arguments) + '): \n\n')

    command = ""
    while command != "quit":
        if command in arguments:
            control.callBack(command)
        elif command and command != "":
            print("Command not found: " + command)
        try:
            command = input().lower()
        except EOFError:
            print("We are in an interface, which does not allow to have text entries")
            while True:
                time.sleep(10000)
