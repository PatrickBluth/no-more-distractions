from threading import Thread
import time
import webbrowser
import winsound

import utils


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


def main():

    active_time, url = user_prompt()

    # opens url using default browser if a complete url is enter, ie. https://www.google.ca, but will open
    # IE if a non complete URL is not complete, ie. google.ca
    webbrowser.open(url)

    utils.key_hook(True)

    blocking_thread = Thread(target=utils.better_listener)
    blocking_thread.daemon = True
    blocking_thread.start()

    time.sleep(active_time)

    utils.key_hook(False)

    # completion alarm in hz and milliseconds
    winsound.Beep(440, 2000)

    print('Congrats, you made it!')


# make sure user is admin
if not admin.isUserAdmin():
        admin.runAsAdmin()
else:
    main()
