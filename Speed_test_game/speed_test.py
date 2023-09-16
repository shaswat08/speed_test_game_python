#creating a typing test game that calculates the word per minute of the given text in the screen. The text in the screen is randomized in every completion. This is done via python.

import curses #importing the curses module
from curses import wrapper
import time #importing the time module
import random #importin the random module

def random_text():

    with open("Random.txt", "r") as f:
        text = f.readlines()
        return random.choice(text).strip()

def start_screen(stdscr):

    stdscr.clear() #clears the screen
    stdscr.addstr("Welcome to the typing text game!") #displays in the screen
    stdscr.addstr("\nPress any key to continue!")
    stdscr.refresh() #refreshes the screen
    stdscr.getkey() #waits for user to press a key

def wpm_screen(stdscr, display, typing, wpm):

    stdscr.addstr(display)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(typing):

        correct_text = display[i]
        color = curses.color_pair(2)

        if char == correct_text:
            stdscr.addstr(0, i, char, color)

        else:
            stdscr.addstr(0, i, char, curses.color_pair(1))

def typing_screen(stdscr):

    display_text = random_text()
    typing_text = []
    wpm = 0
    stdscr.nodelay(True)

    start_time = time.time() #initial time before the loop

    while True:

        elapsed_time = max(time.time() - start_time, 1) #time after the loop starts
        wpm = round((len(typing_text) / (elapsed_time / 60)) / 5) #formula to calculate the words per minute

        stdscr.clear()
        wpm_screen(stdscr, display_text, typing_text, wpm)
        stdscr.refresh()

        if "".join(typing_text) == display_text:
            stdscr.nodelay(False)
            break
        
        try:
            key = stdscr.getkey() #exception handling

        except:
            continue

        if ord(key) == 27: #creating a way for the player to exit the program if they press the escape key
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"): #creating a backspace function
            
            if len(typing_text) > 0:
                typing_text.pop()
        
        elif len(typing_text) < len(display_text):
            typing_text.append(key) #appending the keys that the user types


def main(stdscr):

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) #makes the text color red and the foreground color black
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True: 
        start_screen(stdscr) #calling the start_screen function
        typing_screen(stdscr) #calling the typing_screen function
        
        stdscr.addstr(3, 0, "You completed it. Press any key to try again!")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)