import keyboard
import os
from timeit import default_timer as timer
import webbrowser
import winsound

# make sure user is admin
import admin
if not admin.isUserAdmin():
        admin.runAsAdmin()


def time_elapsed(start_time, timer):
    return timer - start_time


def main():
    while True:
        try:
            # Get input time in seconds and convert to minutes
            active_time_secs = input('How many minutes would you like to be blocked for? '
                                     'Enter number or "q" to quit: ')
            active_time = float(active_time_secs) * 60

            # quit if q is entered
            if active_time_secs.lower() == 'q':
                print('Exiting...')
                return

            # check if valid input
            if type(active_time) != float:
                raise ValueError
            else:
                break

        except ValueError:
            print('Invalid input. Enter a number of minutes, ie. 30')

    # open desired webpage
    url = input('Enter desired website url :')
    webbrowser.open(url)

    # set current time as starting time
    start_time = timer()

    Make window full-screen and block keys used to exit
    keyboard.press_and_release('f11')
    keyboard.block_key('f11')
    keyboard.block_key('windows')
    keyboard.remap_hotkey('alt+tab', 'shift')
    keyboard.remap_hotkey('alt+f4', 'shift')

    # While timer still active continue blocking
    while time_elapsed(start_time, timer()) < active_time:
        os.system('taskkill /im Taskmgr.exe')
        pass

    # un-full-screen
    keyboard.press_and_release('f11')

    # Completion alarm
    duration = 2000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    print('Congrats, you made it!')


main()
