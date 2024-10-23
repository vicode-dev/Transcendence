import curses

class Prompt:

    def __init__(self, stdscr, textDisplay, placeHolder, checkFunc):
        self._stdscr = stdscr
        self._textDisplay = textDisplay
        self._placeHolder = placeHolder
        self._checkFunc = checkFunc

    
    
