import csv
import keyboard
import mouse
import os
import subprocess
from timeit import default_timer as timer
import time
import webbrowser
import winsound

# package by Preston Landers to check if user is running as admin
import admin


def time_elapsed(start_time, timer):
    return timer - start_time

def detect_task_manager():

    p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True)

    for p in csv.DictReader(p_tasklist.stdout):
        if p['Image Name'] == 'Taskmgr.exe':
            return True
    return False

def key_hook(arg):
    if arg:
        # Make window full-screen and block keys used to exit
        # Windows stops ctrl+alt+del from being remapped
        keyboard.press_and_release('f11')
        keyboard.block_key('f11')
        keyboard.block_key('windows')
        keyboard.remap_hotkey('alt+tab', 'shift')
        keyboard.remap_hotkey('alt+f4', 'shift')
    else:
        keyboard.press_and_release('f11')
        keyboard.unhook_all()
    return

def main():
    while True:
        try:
            # time in seconds
            active_time_secs = input('How many minutes would you like to be blocked for? '
                                     'Enter number or "q" to quit: ')
            if active_time_secs.lower() == 'q':
                print('Exiting...')
                return

            active_time = float(active_time_secs) * 60

            if type(active_time) != float:
                raise ValueError
            else:
                break

        # loop through prompt until response is a number
        except ValueError:
            print('Invalid input. Enter a number of minutes, ie. 30')

    # opens url using default browser if a complete url is enter, ie. https://www.google.ca, but will open
    # IE if a non complete URL is not complete, ie. google.ca
    url = input('Enter full URL of desired website: ')
    webbrowser.open(url)

    key_hook(True)

    # start clock once web page has been opened
    start_time = timer()

    while time_elapsed(start_time, timer()) < active_time:
        # close task manager if open
        os.system('taskkill /im Taskmgr.exe')

        if detect_task_manager():
                 current_time = timer()
                 while current_time + 3 > timer():
                     mouse.move(1, 1)

    key_hook(False)

    # completion alarm in hz and milliseconds
    winsound.Beep(440, 2000)

    print('Congrats, you made it!')
    input('press enter to end the program')


# make sure user is admin
if not admin.isUserAdmin():
        admin.runAsAdmin()
else:
    main()
