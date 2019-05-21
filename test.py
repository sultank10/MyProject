#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# title            :menu.py
# description     :This program displays an interactive menu on CLI
# author          :Kevin Fong
# date            :19 May 2019
# version          :0.1
# usage           :python menu.py
# notes           :
# =======================================================================

# Import the modules needed to run the script.


import csv
import os
import sys
import pexpect
from contextlib import contextmanager

# Temporarily suppress output
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


# Main definition - constants
menu_actions = {}

# =======================
#     MENUS FUNCTIONS
# =======================

# Main menu


def main_menu():
    os.system('clear')

    print("Welcome\n".center(80))
    print("Please choose from menu:".center(80))
    print("\n")
    print("1. Diagnose")
    print("2. Remote Connect via SSH")
    print("0. Quit")
    print("\n")
    choice = input(" >>  ")
    exec_menu(choice)

    return

# Execute menu


def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return

# Menu 1


def menu1():
    print("Diagnosis Menu\n".center(80))
    print("1. Ping")
    print("9. Return to Menu")
    print("0. Quit")
    print("\n")
    choice = input(" >>  ")
    if choice == "1":
        ping_menu()
    elif choice == "9":
        back()
    elif choice == "0":
        exit()
    return

# Menu 2


def menu2():
    print("SSH to Host\n".center(70))
    print("1. Train")
    print("2. Management Servers")
    print("9. Back")
    print("0. Quit")
    print("\n")
    choice = input(" >>  ")
    if choice == "1":
        ssh()
    else:
        exec_menu(choice)
    return

# Ping Menu


def ping_menu():
    os.system('clear')
    print("Ping Menu\n".center(70))
    print("1. All Trains")
    print("2. Select Train")
    print("9. Return to Menu")
    print("0. Quit")
    print("\n")
    choice = input(" >> ")
    if choice == "1":
        ping_all_trains()
    elif choice == "2":
        ping_selected_train()
    elif choice == "9":
        back()
    elif choice == "0":
        exit()
    return

# Ping command


def ping_all_trains():
    os.system('clear')

    # read file
    f = open('ipList.csv', 'r')
    reader = csv.reader(f)

    for row in reader:
        if row[0] == "name":
            pass
        else:
            print("Pinging {}...".format(row[0]))
            output = os.system("ping -c 1 " + row[1] + " >/dev/null 2>&1")
            # and then check the response...
            if output == 0:
                print("{} is up".format(row[0]))
            else:
                print("{} is unreachable".format(row[0]))
    input("\n Press Enter to return to Menu")
    submenu()

# Ping Selected Train


def ping_selected_train():
    os.system('clear')

    login = "matrail@10.99.99.1"
    psswd = "wifiBART07"

    with suppress_stdout():
        l = pexpect.spawn("ssh " + login)
        l.expect(["matrail@10.99.99.1\'s password:", pexpect.EOF])
        l.sendline(psswd)
    l.expect("$")
    global global_pexpect_instance
    global_pexpect_instance = l

    with open('ipList.csv') as fobj:
        text = fobj.read().strip().split()
        while True:
            try:
                s = input("Enter IP address: ")
                if s == "":
                    continue
                if s in text:
                    pr = l.sendline("ping -c 1 " + s)
                    if pr == 0:
                        print("Host is Up")
                    else:
                        print("Host is Down")
                    l.expect("$")
                    l.sendline("exit")
                    l.interact()
                    break
                raise Exception("IP address invalid, try again")
            except Exception as e:
                print(e)


# SSH to host


def ssh():
    os.system('clear')

    print("Enter a mig number: EG. mig1 ")
    mig = input()

    p = pexpect.spawn("ssh " + mig)

    i = p.expect(["matrail@10.99.99.1\'s password:", pexpect.EOF])
    if i == 0:
        p.sendline("wifiBART07")
    elif i == 1:
        print("unreachable")
        pass
    elif i == 2:
        print("timeout")
        pass
    global global_pexpect_instance
    global_pexpect_instance = p
    try:
        p.interact()
        sys.exit(0)
    except:
        sys.exit(1)
    print("Press Enter to return to Menu")
    submenu()

# Back to main menu


def back():
    menu_actions['main_menu']()

# Back to previous menu


def submenu():
    os.system('clear')
    ping_menu()

# Exit program


def exit():
    sys.exit()

# =======================
#    MENUS DEFINITIONS
# =======================


# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '9': back,
    '0': exit,
}

# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
