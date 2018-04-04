from timeit import default_timer as timer
import webbrowser
import winsound


def time_elapsed(start_time, timer):
    return timer - start_time


def main():
    while True:
        try:
            # Get input time
            active_time = input('How many minutes would you like to be blocked for? Enter number or "q" to quit: ')
            if active_time.lower() == 'q':
                print('Exiting...')
                return

            # check if valid input
            if type(int(active_time)) != int:
                raise ValueError
            else:
                active_time = int(active_time)
                break

        except ValueError:
            print('Invalid input. Enter a number of minutes, ie. 30')

    # open desired webpage
    url = input('Enter desired website url :')
    webbrowser.open(url)

    # set current time as starting time
    start_time = timer()

    # While timer still active
    while time_elapsed(start_time, timer()) < active_time:
        f

    # Completion alarm
    duration = 2000  # millisecond
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    print('Congrats, you made it!')


main()
