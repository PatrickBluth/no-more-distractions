import keyboard
import mouse
import os
import pythoncom
import time
import wmi

from threading import Thread
from stoppable_thread import PausableThread


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
    while True:
        mouse.move(1, 1)
        time.sleep(0.01)
        # current_time = timer()
        # # lock mouse in top left corner for 3 seconds
        # while current_time + duration > timer():
        #     mouse.move(1, 1)


def listener():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    process_watcher = c.Win32_Process.watch_for("creation")
    while True:
        new_process = process_watcher()
        if new_process.Caption == 'Taskmgr.exe':
            mouse_lock()
            os.system('taskkill /im Taskmgr.exe')


def better_listener():
    pythoncom.CoInitialize()
    c = wmi.WMI()
    creation_watcher = c.Win32_Process.watch_for("creation")
    deletion_watcher = c.Win32_Process.watch_for("deletion")
    t = PausableThread()
    t.start()  # starts paused
    t.pause()  # needs to setup with pause function before running
    while True:
        new_process = creation_watcher()
        old_process = deletion_watcher()
        if new_process.Caption == 'LogonUI.exe':
            t.resume()
            while True:
                old_process = deletion_watcher()
                new_process = creation_watcher()

                if old_process.Caption == 'LogonUI.exe' or new_process.Caption == 'Taskmgr.exe':
                    break
            os.system('taskkill /im Taskmgr.exe')
            t.pause()
