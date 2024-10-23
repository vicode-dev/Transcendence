import tomllib
from menu.Menu import Menu
def configLoad():
    configFile = open("config.toml", "rb")
    data = tomllib.load(configFile)
    return data

def serverURL(menu):
    return

def settings(menu):
    name = ["Server URL"]
    func = [serverURL]
    menu = Menu(menu.win, "Settings", name, func)
    menu.display()
    return