# package imports
import csv
import keyboard
import mouse
import os
import subprocess
from timeit import default_timer as timer
import webbrowser
import winsound

# import admin class
import admin


def time_elapsed(start_time, timer):
    return timer - start_time


def freeze_mouse(event):
    return False


def main():
    while True:
        try:
            # Get input time in seconds
            active_time_secs = input('How many minutes would you like to be blocked for? '
                                     'Enter number or "q" to quit: ')
            # quit if q is entered
            if active_time_secs.lower() == 'q':
                print('Exiting...')
                return

            # contert input time into minutes
            active_time = float(active_time_secs) * 60

            # check if valid input
            if type(active_time) != float:
                raise ValueError
            else:
                break

        # loop through prompt until response is a number
        except ValueError:
            print('Invalid input. Enter a number of minutes, ie. 30')

    # open desired webpage
    url = input('Enter desired website url :')
    webbrowser.open(url)

    # set current time as starting time
    start_time = timer()

    # Make window full-screen and block keys used to exit
    keyboard.press_and_release('f11')
    keyboard.block_key('f11')
    keyboard.block_key('windows')
    keyboard.remap_hotkey('alt+tab', 'shift')
    keyboard.remap_hotkey('alt+f4', 'shift')

    # While timer still active continue blocking
    while time_elapsed(start_time, timer()) < active_time:

        # close task manager if open
        os.system('taskkill /im Taskmgr.exe')

        # determine if task manager is opened
        p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                                      stdout=subprocess.PIPE,
                                      universal_newlines=True)

        for p in csv.DictReader(p_tasklist.stdout):
            # if task manager opened prevent user from using mouse for 3 seconds
            if p['Image Name'] == 'Taskmgr.exe':
                current_time = timer()
                while current_time + 3 > timer():
                    mouse.move(1, 1)

    # un-full-screen
    keyboard.press_and_release('f11')
    keyboard.unhook_all()

    # Completion alarm
    duration = 2000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    print('Congrats, you made it!')
    input('press enter to end the program')


# make sure user is admin
if not admin.isUserAdmin():
        admin.runAsAdmin()

main()
