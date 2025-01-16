from network.config import configLoad
from websockets.sync.client import connect
from threading import Thread
import requests, ssl, json, curses

playersList = []
maxPlayers = None
def createLobby(jwt, gameType):
    config = configLoad()
    response = requests.post(f"https://{config['server']['url']}/lobby/api/create/?gameType={gameType}", headers={'Cookie': f"session={jwt}"})
    if response.status_code != 200:
        raise Exception(response.text)
    response = response.json()
    return response["id"]

def lobby_websocket(jwt, id):
    global playersList
    global maxPlayers
    config = configLoad()
    ssl_context = ssl.create_default_context()
    with connect(f"wss://{config['server']['url']}/ws/lobby/{id}/", additional_headers={"Cookie": f"session={jwt}"}, ssl=ssl_context, origin=f"https://{config['server']['url']}") as websocket:
        while True:
            messageStr = websocket.recv()
            message = json.loads(messageStr)
            match message["type"]:
                case "lobby_game":
                    playersList = getPlayersList(jwt, message["players"])
                    maxPlayers = message["maxPlayers"]
                case "lobby_redirect":
                    break
    return

def lobby(win, id, jwt):
    global playersList
    global maxPlayers
    config = configLoad()
    thread = Thread(target = lobby_websocket, args = (jwt, id))
    thread.start()
    win.nodelay(True)
    while True:
        win.erase()
        win.addstr(0,0, f"Lobby {id}")
        win.addstr(1,0, f"Players: {len(playersList)}/{maxPlayers}")
        for i in range(len(playersList)):
            win.addstr(i + 2, 0, playersList[i])    
        win.refresh()
        key = win.getch()
        if(key == ord('q')):
            break
        if(key == ord('2') and maxPlayers != 2):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?maxPlayers=2", headers={'Cookie': f"session={jwt}"})
        if(key == ord('4') and maxPlayers != 4):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?maxPlayers=4", headers={'Cookie': f"session={jwt}"})
        if((key == ord('l') or key == ord('e')) and playersList == maxPlayers):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/start/", headers={'Cookie': f"session={jwt}"})
        if(key == ord('p')):
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?private=0", headers={'Cookie': f"session={jwt}"})
            requests.post(f"https://{config['server']['url']}/lobby/{id}/?private=1", headers={'Cookie': f"session={jwt}"})
    thread._stop()
    thread.join()
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