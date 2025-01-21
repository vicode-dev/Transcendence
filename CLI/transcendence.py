import curses, sys, re
import signal
from curses import wrapper
from menu.Menu import Menu
from menu.Prompt import Prompt
from pong.twoPlayers import gameLoop2P, gameLoopBot2P
from pong.fourPlayers import gameLoop4P, SIZE
from connect4.connect4 import gameConnectLoop,gameConnectLoopAi
from network.login import login
from network.config import settings, configLoad
from network.lobby import createLobby, lobby

jwt = None
# Define a handler function that does nothing
def ignore_sigint(signum, frame):
    pass

signal.signal(signal.SIGTSTP, ignore_sigint)
signal.signal(signal.SIGQUIT, ignore_sigint)
signal.signal(signal.SIGINT, quit)



def cursesInit():
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    curses.set_escdelay(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(3, 8, curses.COLOR_BLACK)

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
    # try:
    gameLoop2P(menu.win, gameWin, pad, scale)
    # except:
    #     menu.win.erase()
    #     menu.win.addstr(0, 0, "Game crashed", )
    #     menu.win.refresh()
    #     curses.napms(500)
    #     menu.win.getch()
    menu.skip = True
    return

def launchIAPong(menu):
	height, width = menu.win.getmaxyx()
	height -= 1
	scale = height - (height % (SIZE)) if height < width else width - (width % SIZE)
	scale = int(scale / 10)
	length = (SIZE * scale) + 2
	menu.win.erase()
	menu.win.refresh()
	gameWin = curses.newwin(length, length, 1, int(width / 2 - length / 2))
	pad = curses.newpad(1, width)
    # try:
	gameLoopBot2P(menu.win, gameWin, pad, scale)
    # except:
    #     menu.win.erase()
    #     menu.win.addstr(0, 0, "Game crashed", )
    #     menu.win.refresh()
    #     curses.napms(500)
    #     menu.win.getch()
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
    # try:
	gameLoop4P(menu.win, gameWin, pad, scale)
    # except:
    #     menu.win.erase()
    #     menu.win.addstr(0, 0, "Game crashed", )
    #     menu.win.refresh()
    #     curses.napms(500)
    #     menu.win.getch()
	menu.skip = True
	return

def launchConnectGame(menu):
    height, width = menu.win.getmaxyx()
    menu.win.erase()
    menu.win.refresh()
    gameWin = curses.newwin(14, 23, 2, int(width / 2 - 23 / 2))
    pad = curses.newpad(1, width)
    gameConnectLoop(menu.win, gameWin, pad)
    menu.skip = True
    return

def launchConnectGameAi(menu):
    height, width = menu.win.getmaxyx()
    menu.win.erase()
    menu.win.refresh()
    gameWin = curses.newwin(14, 23, 2, int(width / 2 - 23 / 2))
    pad = curses.newpad(1, width)
    gameConnectLoopAi(menu.win, gameWin, pad)
    menu.skip = True
    return
    
    
def pongNewGame(mainmenu):
    menu = Menu(mainmenu.win, "New Game:", ["2P", "4P","Ai opponent"], [launchGame2P, launchGame4P, launchIAPong])
    menu.display()

def connect4NewGame(mainmenu):
	menu = Menu(mainmenu.win, "New Game:", ["2P", "Ai opponent"], [launchConnectGame, launchConnectGameAi])
	menu.display()

def Offline(mainmenu):
    menu = Menu(mainmenu.win, "New Game:", ["Pong", "Connect 4"], [pongNewGame, connect4NewGame])
    menu.display()

def Online(menu):
    global jwt
    if jwt == None:
        return
    menu = Menu(menu.win, "Online", ["Create a lobby", "Join"], [lobbySelector, Join])
    menu.display()

def checkGameUrl(input):
    if input == None:
        return False
    serv = configLoad()["server"]["url"]
    url_pattern = fr"https://{serv}/lobby/[0-9a-f]{{8}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{4}}-[0-9a-f]{{12}}/$"
    res = re.fullmatch(url_pattern, input)
    if res:
        return True
    else:
        return False

def Join(menu):
    global jwt

    serv = configLoad()["server"]["url"]

    prompt = Prompt(menu.win, "Enter the game URL " + serv + ".", None, checkGameUrl)
    prompt.display()
    url = prompt.input
    if (url != None and url != ""):
        url = (url.split('/'))[4]
        lobby(menu.win, url, jwt)
    return

def lobbySelector(menu):
    menu.skip = True
    menu = Menu(menu.win, "GameType", ["Pong", "Connect 4"], [createLobbyPong, createLobbyConnect4])
    menu.display()
    return

def createLobbyPong(menu):
    global jwt
    menu.skip = True
    try:
        lobbyId = createLobby(jwt, 0)
    except Exception as e:
        curses.endwin()
        print(e)
        sys.exit(1)
    lobby(menu.win, lobbyId, jwt)
    return

def createLobbyConnect4(menu):
    global jwt
    menu.skip = True
    try:
        lobbyId = createLobby(jwt, 1)
        lobby(menu.win, lobbyId)
    except Exception as e:
        curses.endwin()
        print(e)
        sys.exit(1)   
    return


def quit(*args):
    curses.endwin()
    print("Exit")
    sys.exit(0)

def loginPrompt(Menu):
    global jwt
    try:
        token = login()
        jwt = token
        Menu.promptArray[3] = "Logout"
        Menu.functionArray[3] = logout
    except Exception as e:
        Menu.win.clear()
        Menu.win.addstr(0, 0, str(e)[:50])
        Menu.win.refresh()
        curses.napms(500)
        Menu.win.getch()
    return

def logout(menu):
    global jwt
    jwt = None
    menu.promptArray[3] = "Login"
    menu.functionArray[3] = loginPrompt
    return

def main(stdscr):
    global jwt
    cursesInit()
    menuTxt = ["Play offline", "Play online", "Settings", "Logout", "Quit"]
    menuFunc = [Offline, Online, settings, logout, quit]
    try:
        token = login()
        jwt = token
    except Exception as e:
        stdscr.clear()
        stdscr.addstr(0, 0, str(e)[:50])
        stdscr.refresh()
        curses.napms(500)
        stdscr.getch()
        menuTxt[3] = "Login"
        menuFunc[3] = loginPrompt
        
    #mainMenu Part
    mainMenu = Menu(stdscr, "🔴 Transcendence CLI 🏓!", menuTxt, menuFunc)
    mainMenu.display()



if __name__=="__main__":
    wrapper(main)