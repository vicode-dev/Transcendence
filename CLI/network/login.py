from network.config import configLoad
import requests

def login():
    config = configLoad()
    if 'token' not in config or 'jsonwebtoken' not in config['token'] or config['token']['jsonwebtoken'] == "":
        raise Exception("Need login for online play")
    auth = requests.get(f"https://{config['server']['url']}/api/authentication/cli/token/?type=ephemeral", headers={'Authorization': config["token"]["jsonwebtoken"]})
    if auth.status_code != 200:
        raise Exception(auth.text)
    auth = auth.json()
    if 'error' in auth:
        raise Exception(auth['error'])
    return auth['token']
