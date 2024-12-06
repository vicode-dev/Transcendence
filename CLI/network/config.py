import tomllib
from menu.Menu import Menu
from menu.Prompt import Prompt

def configLoad():
    configFile = open("config.toml", "rb")
    data = tomllib.load(configFile)
    return data

def checkURL(input):
    if (input == "qqq"):
        return True
    return False

def serverURL(menu):
    s = "Enter the server URL"
    prompt = Prompt(menu.win, s, "www.transcendence.vicode", checkURL)
    prompt.display()
    return

def settings(menu):
    name = ["Server URL"]
    func = [serverURL]
    menu = Menu(menu.win, "Settings", name, func)
    menu.display()
    return