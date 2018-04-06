from axel import Event
import csv
import keyboard
import mouse
import os
import subprocess
from tkinter import *
from tkinter import ttk
from timeit import default_timer as timer
import time
import webbrowser
import winsound

import admin  # package by Preston Landers to check if user is running as admin


class AppManager(Frame):

    def __init__(self):
        Frame.__init__(self)
        mainframe = ttk.Frame(self, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        active_time = StringVar()
        self.active_time = active_time # in seconds
        active_time_entry = ttk.Entry(mainframe, width=7, textvariable=active_time)
        active_time_entry.grid(column=2, row=1, sticky=(W, E))

        url = StringVar()
        self.url = url
        url_entry = ttk.Entry(mainframe, width=7, textvariable=url)
        url_entry.grid(column=2, row=2, sticky=(W, E))

        ttk.Button(mainframe, text="Start!", command=self.coordinator).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="Desired Time (min)").grid(column=1, row=1, sticky=E)
        ttk.Label(mainframe, text="URL").grid(column=1, row=2, sticky=E)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        active_time_entry.focus()

    @staticmethod
    def time_elapsed(start_time, timer):
        return timer - start_time

    @staticmethod
    def detect_task_manager():

        p_tasklist = subprocess.Popen('tasklist.exe /fo csv',
                                      stdout=subprocess.PIPE,
                                      universal_newlines=True)

        for p in csv.DictReader(p_tasklist.stdout):
            if p['Image Name'] == 'Taskmgr.exe':
                return True
        return False

    @staticmethod
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

    @staticmethod
    def mouse_lock():
        current_time = timer()
        while current_time + 3 > timer():
            mouse.move(1, 1)

    def coordinator(self):

        active_time = int(self.active_time.get())

        # opens url using default browser if a complete url is enter, ie. https://www.google.ca, but will open
        # IE if a non complete URL is not complete, ie. google.ca
        webbrowser.open(self.url.get())

        self.key_hook(True)

        # start clock once web page has been opened
        start_time = timer()

        while self.time_elapsed(start_time, timer()) < active_time:
            time.sleep(60)
            # close task manager if open
            os.system('taskkill /im Taskmgr.exe')

            if self.detect_task_manager():
                self.mouse_lock()

        self.key_hook(False)

        # completion alarm in hz and milliseconds
        winsound.Beep(440, 2000)

        print('Congrats, you made it!')
        input('press enter to end the program')


def main():
    root = Tk()
    root.title("No More Distractions")
    AppManager().pack(fill="both", expand=True)
    root.mainloop()

# make sure user is admin
if not admin.isUserAdmin():
        admin.runAsAdmin()
else:
    main()


