import curses, sys
from curses import wrapper
from menu.Menu import Menu
from pong.twoPlayers import gameLoop2P
from pong.fourPlayers import gameLoop4P
from network.login import login
from network.config import settings
SIZE= 9

def cursesInit():
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.set_escdelay(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN)

def launchGame2P(menu):
    height, width = menu.win.getmaxyx()
    height -= 1
    scale = height - (height % (SIZE)) if height < width else width - (width % SIZE)
    scale = int(scale / 10)
    length = (SIZE * scale) + 2
    menu.win.erase()
    menu.win.refresh()
    gameWin = curses.newwin(length, length, 1, int(width / 2 - length / 2))
    pad = curses.newpad(1, width)
    try:
        gameLoop2P(menu.win, gameWin, pad, scale)
    except:
        menu.win.erase()
        menu.win.addstr(0, 0, "Game crashed", )
        menu.win.refresh()
        curses.napms(500)
        menu.win.getch()
    menu.skip = True
    return

def launchGame4P(menu):
    height, width = menu.win.getmaxyx()
    height -= 1
    scale = height - height % SIZE if height < width else width - width % SIZE
    scale = int(scale / 10)
    length = (SIZE * scale) + 2
    menu.win.erase()
    menu.win.refresh()
    gameWin = curses.newwin(length, length, 1, int(width / 2 - length / 2))
    pad = curses.newpad(1, width)
    try:
        gameLoop4P(menu.win, gameWin, pad, scale)
    except:
        menu.win.erase()
        menu.win.addstr(0, 0, "Game crashed", )
        menu.win.refresh()
        curses.napms(500)
        menu.win.getch()
    menu.skip = True
    return

def NewGame(mainmenu):
    menu = Menu(mainmenu.win, "New Game:", ["2P", "4P"], [launchGame2P, launchGame4P])
    menu.display()

def join(Menu):
    return

def logout(Menu):
    return

def quit(Menu):
    sys.exit(0)

def main(stdscr):
    cursesInit()
    login()
    #mainMenu Part
    menuTxt = ["New Game", "Join Game", "Settings", "Logout", "Quit"]
    menuFunc = [NewGame, join, settings, logout, quit]
    mainMenu = Menu(stdscr, "Pong CLI 🏓!", menuTxt, menuFunc)
    mainMenu.display()



if __name__=="__main__":
    wrapper(main)