import tomllib, toml
from menu.Menu import Menu
from menu.Prompt import Prompt

def configLoad():
    with open("config.toml", "rb") as configFile:
        data = tomllib.load(configFile)
        return data

def configSave(data):
    with open("config.toml", "w") as configFile:
        toml.dump(data, configFile)
    return
def checkURL(input):
    if (input == "qqq"):
        return False
    return True

def checkToken(input):
    if (len(input) > 0 ):
        return True
    return False

def serverURL(menu):
    s = "Enter the server URL"
    config = configLoad()
    if 'server' in config and 'url' in config['server'] and config['server']['url'] != "":
        placeholder = config['server']['url']
    else:
        placeholder = "www.transcendence.example.com"
    prompt = Prompt(menu.win, s, placeholder, checkURL)
    prompt.display()
    if prompt.input != "":
        config['server']['url'] = prompt.input
        configSave(config)
    return

def token(menu):
    s = "Enter the auth token"
    config = configLoad()
    if 'token' in config and 'jsonwebtoken' in config['token'] and config['token']['jsonwebtoken'] != "":
        placeholder = config['token']['jsonwebtoken']
    else:
        placeholder = "Check settings page on web"
    prompt = Prompt(menu.win, s, placeholder, None)
    prompt.display()
    if prompt.input != "":
        config['token']['jsonwebtoken'] = prompt.input
        configSave(config)
    return

def settings(menu):
    name = ["Server URL", "Token"]
    func = [serverURL, token]
    menu = Menu(menu.win, "Settings", name, func)
    menu.display()
    return