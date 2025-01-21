import curses
from curses.textpad import Textbox

class Prompt:

    def __init__(self, stdscr, textDisplay, placeHolder, checkFunc, widthBorder = 3):
        self.stdscr = stdscr
        self.textDisplay = textDisplay
        self.placeHolder = placeHolder # default text in textbox
        self.checkFunc = checkFunc
        self.input = ""
        self.widthBorder = widthBorder
        self.exit = False

    # def enter(self, key):
    #     if key == 27:
    #         self.exit = True
    #     if key == 27 or key == 10:
    #         return 7
    #     if key == 263:
    #         return 4
    #     if key == curses.KEY_LEFT:
    #         return 2
    #     if key == curses.KEY_RIGHT:
    #         return 6

    def displayPrompt(self, width, height, startW, startH):
        sen = self.textDisplay.split('\n')
        for i in range(len(sen)):
            if (startH >= height):
                return startH
            if len(sen[i]) < width - 2 * self.widthBorder:
                self.stdscr.addstr(startH, startW, sen[i])
            else:
                startWidth = startW
                words = sen[i].split(' ')
                for j in range(len(words)):
                    words[j] += " "
                    if (len(words[j]) + startWidth < width - self.widthBorder):
                        self.stdscr.addstr(startH, startWidth, words[j])
                        startWidth += len(words[j])
                    else:
                        self.stdscr.addch(startH, startWidth, '\n')
                        startH += 1
                        if (startH >= height):
                            return startH
                        startWidth = startW
                        if (len(words[j]) > width - 2 * self.widthBorder):
                            for letter in words[j]:
                                if (startWidth + 1 < width - 2 * self.widthBorder):
                                    self.stdscr.addch(startH, startWidth, letter)
                                else:
                                    self.stdscr.addch(startH, startWidth, '\n')
                                    startWidth = startW
                                    startH += 1
                                    if (startH >= height):
                                        return startH
                                    self.stdscr.addch(startH, startWidth)
                                startWidth += 1
                        else:
                            self.stdscr.addstr(startH, startWidth, words[j])
                            startWidth += len(words[j])
            startH += 1
        return startH

    # def getInput(self, win, box, newH, width):
    #     self.exit = False
    #     win.clear()
    #     win.refresh()
    #     self.input = ""
    #     box.edit(self.enter)
    #     self.input = box.gather().strip()
    #     if self.exit == True:
    #         if (self.input == ""):
    #             self.input = self.placeHolder

    def getInput(self, win, pad, width, height):
        win.keypad(True)
        key = win.getch()
        cursor = 0
        curses.curs_set(1)
        curses.setsyx(height, cursor + self.widthBorder)
        curses.doupdate()
        while (key != 10 and key != curses.KEY_UP):
            if key ==  curses.KEY_RIGHT:
                if cursor < len(self.input):
                    cursor += 1
            elif key == curses.KEY_LEFT:
                if cursor > 0:
                    cursor -= 1
            if key == 27:
                self.input = self.placeHolder
                return True
            elif key == curses.KEY_BACKSPACE or key == curses.KEY_DOWN:
                if cursor > 0:
                    self.input = self.input[:cursor - 1] + self.input[cursor:]
                    cursor -= 1
                    pad.clear()
                    pad.addstr(0, 0, self.input)
                    pad.refresh(0, 0, height, self.widthBorder, height, width - self.widthBorder)
            elif key >= 32 and key <= 126:
                self.input = self.input[:cursor] + chr(key) + self.input[cursor:]
                cursor += 1
                pad.addstr(0, 0, self.input)
                pad.refresh(0, 0, height, self.widthBorder, height, width - self.widthBorder)
            curses.setsyx(height, cursor + self.widthBorder)
            curses.doupdate()
            key = win.getch()
        if (self.checkFunc and self.checkFunc(self.input) == False):
            self.input = ""
            return False
        else:
            return True

    def display(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        newH = self.displayPrompt(width - self.widthBorder, height - 1, self.widthBorder, 0)
        if (newH + 2 < height):
            newH += 2
        win = curses.newwin(1, width - 2 * self.widthBorder, newH - 1, self.widthBorder)
        self.stdscr.refresh()
        if width < 300:
            newW = 300
        else:
            newW = width
        pad = curses.newpad(10, newW)
        win.clear()
        if self.placeHolder != None:
            s = "Default value: " + self.placeHolder + " (press any key to edit)"
        else:
            s = "(press any key to edit)"
        curses.raw(True)
        pad.addstr(0, 0, s, curses.color_pair(3))
        pad.refresh(0, 0, newH, self.widthBorder, newH, width - self.widthBorder)
        win.refresh()
        if win.getch() != 27:
            while True:
                pad.clear()
                pad.refresh(0, 0, newH, self.widthBorder, newH, width - self.widthBorder)
                if self.getInput(win, pad, width, newH) == True:
                    curses.curs_set(0)
                    return
