import csv
import keyboard
import mouse
import os
import pythoncom
import signal
import subprocess
from threading import Thread
from timeit import default_timer as timer
import time
import webbrowser
import winsound
import wmi



# package by Preston Landers to check if user is running as admin
import admin


def user_prompt():
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

    url = input('Enter full URL of desired website: ')
    return active_time, url


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
        # keyboard.press_and_release('f11')
        keyboard.block_key('f11')
        keyboard.block_key('windows')
        keyboard.remap_hotkey('alt+tab', 'shift')
        keyboard.remap_hotkey('alt+f4', 'shift')
    else:
        keyboard.press_and_release('f11')
        keyboard.unhook_all()


def mouse_lock():
    current_time = timer()
    while current_time + 3 > timer():
        mouse.move(1, 1)


def listener():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for("creation")
    while True:
        new_process = process_watcher()
        print(new_process.Caption)
        if new_process.Caption == 'Taskmgr.exe':
            os.system('taskkill /im Taskmgr.exe')
            mouse_lock()


def task_manager_block_fast():


    p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                                  stdout=subprocess.PIPE,
                                  universal_newlines=True)
    while True:
        time.sleep(0.05)

        wql = 'SELECT * FROM Win32_Process WHERE Name LIKE "%chrome%"'

        # p_temp = subprocess.Popen('tasklist.exe /fo csv',
        #                           stdout=subprocess.PIPE,
        #                           universal_newlines=True)
        #
        # if p_tasklist != p_temp:
        #     p_tasklist = p_temp
        #     for p in csv.DictReader(p_tasklist.stdout):
        #         if p['Image Name'] == 'Taskmgrr.exe':
        #             os.system('taskkill /im Taskmgr.exe')


def task_manager_block():

    while True:
        if detect_task_manager():
            os.system('taskkill /im Taskmgr.exe')
            mouse_lock()


def main():

    active_time, url = user_prompt()

    # opens url using default browser if a complete url is enter, ie. https://www.google.ca, but will open
    # IE if a non complete URL is not complete, ie. google.ca
    webbrowser.open(url)

    key_hook(True)

    # start clock once web page has been opened
    start_time = timer()

    blocking_thread = Thread(target=listener)
    blocking_thread.daemon = True
    blocking_thread.start()

    time.sleep(active_time)

    key_hook(False)

    # completion alarm in hz and milliseconds
    winsound.Beep(440, 2000)

    print('Congrats, you made it!')


# make sure user is admin
if not admin.isUserAdmin():
        admin.runAsAdmin()
else:
    main()
