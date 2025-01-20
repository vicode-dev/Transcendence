from network.config import configLoad
from websockets.sync.client import connect
from threading import Thread
from pong.twoPlayersOnline import gameLoop2P
from pong.fourPlayersOnline import gameLoop4P
from connect4.connect4Online import gameConnectLoop
import requests, json, curses

playersList = []
maxPlayers = None
start = False
def createLobby(jwt, gameType):
    config = configLoad()
    response = requests.post(f"https://{config['server']['url']}/lobby/api/create/?gameType={gameType}", headers={'Cookie': f"session={jwt}"})
    if response.status_code != 200:
        raise Exception(response.text)
    response = response.json()
    return response["id"]

def lobby_websocket(jwt, id, websocket):
    global playersList
    global maxPlayers
    global start
    while True:
        messageStr = websocket.recv()
        message = json.loads(messageStr)
        match message["type"]:
            case "lobby_game":
                playersList = getPlayersList(jwt, message["players"])
                maxPlayers = message["maxPlayers"]
            case "lobby_redirect":
                start = True
                break
    return

def lobby(win, id, jwt):
    global playersList
    global maxPlayers
    global start
    config = configLoad()
    websocket = connect(f"wss://{config['server']['url']}/ws/lobby/{id}/", additional_headers={"Cookie": f"session={jwt}"}, origin=f"https://{config['server']['url']}")
    thread = Thread(target = lobby_websocket, args = (jwt, id, websocket))
    thread.start()
    win.nodelay(True)
    start = False
    while True:
        win.erase()
        win.addstr(0,0, f"Lobby {id}")
        win.addstr(1,0, f"Players: {len(playersList)}/{maxPlayers}")
        for i in range(len(playersList)):
            win.addstr(i + 2, 0, playersList[i])    
        win.refresh()
        key = win.getch()
        if(key == ord('q')):
            websocket.close()
            break
        if(key == ord('2') and maxPlayers != 2):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?maxPlayers=2", headers={'Cookie': f"session={jwt}"})
        if(key == ord('4') and maxPlayers != 4):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?maxPlayers=4", headers={'Cookie': f"session={jwt}"})
        if((key == ord('l') or key == ord('e')) and len(playersList) == maxPlayers):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/start/", headers={'Cookie': f"session={jwt}"})
        if(key == ord('p')):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?private=0", headers={'Cookie': f"session={jwt}"})
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?private=1", headers={'Cookie': f"session={jwt}"})
        if start == True:
            response = requests.get(f"https://{config['server']['url']}/game/{id}/api", headers={'Cookie': f"session={jwt}"}).json()
            if response["gameType"] == False:
                if response["maxPlayers"] == 2:
                    gameLoop2P(win, id, jwt)
                else:
                    gameLoop4P(win, id, jwt)
            else:
                gameConnectLoop(win, id, jwt)
    thread.join()
    win.nodelay(False)
    return

def getPlayersList(jwt, playersId):
    players = []
    config = configLoad()
    for id in playersId:
        response = requests.get(f"https://{config['server']['url']}/api/player/{id}/username/", headers={'Cookie': f"session={jwt}"})
        if response.status_code == 200:
            response = response.json()
            players.append(response["username"])
    return players