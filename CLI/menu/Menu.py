import curses
class Menu:
    def __init__(self, win, title, promptArray, functionArray):
        if len(promptArray) != len(functionArray):
            raise IndexError("promptArray and functionArray differ")
        self.win = win
        self.title = title
        self.promptArray = promptArray
        self.functionArray = functionArray
        self.len = len(promptArray)
        self.selector = 0
        self.skip = False

    def move(self, key):
        if key == curses.KEY_UP or key == ord('w'):
            self.selector = (self.len + self.selector - 1) % self.len
        elif key == curses.KEY_DOWN or key == ord('s'):
            self.selector = (self.selector + 1) % self.len
        elif key == ord('e') or key == curses.KEY_RIGHT:
            self.functionArray[self.selector](self)
        

    def display(self):
        while True:
            self.win.clear()
            height, width = self.win.getmaxyx()
            self.win.addstr(0, width // 2 - (len(self.title) // 2), self.title)
            for i in range(0, self.len):
                if (self.selector != i):
                    self.win.addstr(i + 1, 0, self.promptArray[i])
                else:
                    self.win.addstr(i + 1, 0, self.promptArray[i], curses.color_pair(1))
            self.win.refresh()
            key = self.win.getch()
            self.move(key)
            if key == curses.KEY_RESIZE:
                curses.resize_term(*self.win.getmaxyx())
            if key == 27 or key == curses.KEY_LEFT:
                return
            if self.skip == True:
                self.skip = False
                break
