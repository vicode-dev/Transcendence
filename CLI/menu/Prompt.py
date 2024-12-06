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

    def enter(self, key):
        if key == 27:
            self.exit = True
        if key == 27 or key == 10:
            return 7
        if key == 263:
            return 4
        if key == curses.KEY_LEFT:
            return 2
        if key == curses.KEY_RIGHT:
            return 6

    def cutWord(self, width, height, startW, startH):
        return startH

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

    def display(self):
        height, width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        newH = self.displayPrompt(width - self.widthBorder, height - 1, self.widthBorder, 0)
        if (newH + 2 < height):
            newH += 2
        self.stdscr.refresh()
        win = curses.newwin(1, width - 2 * self.widthBorder, newH, self.widthBorder)
        win.clear()
        s = "Default value: " + self.placeHolder + " (press any key to edit)"
        i = 0
        while (i < width - 2 * self.widthBorder - 2 and i < len(s)):
            win.addch(0, i, s[i], curses.color_pair(3))
            i += 1
        win.refresh()
        if win.getch() != 27:
            box = Textbox(win)
            curses.echo()
            curses.curs_set(1) #setsyx & getsyx ?
            while self.checkFunc(self.input) == False:
                self.exit = False
                win.clear()
                win.refresh()
                self.input = ""
                box.edit(self.enter)
                self.input = box.gather().strip()
                if self.exit == True:
                    self.input = self.placeHolder
                    break
            curses.noecho()
            curses.curs_set(0)


    
