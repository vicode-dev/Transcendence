from web3 import Web3
from profile.models import User
import json
import logging
logger = logging.getLogger('profile')
Contract = None
w3 = None

class Game:
    def __init__(self, _gameId, _playerIds, _score, _gameType, _startTime, _endTime):
        self.gameId = _gameId
        self.playerIds = _playerIds
        self.gameType = _gameType
        self.score = _score
        self.startTime = _startTime
        self.endTime = _endTime
    def to_dict(self):
        return ({"gameId": self.gameId, "playerIds": self.playerIds, "gameType": self.gameType, "score": self.score, "startTime": self.startTime, "endTime": self.endTime })

class Tournament:
    def __init__(self, _tournamentId, _gameIds, _playerIds):
        self.tournamentId = _tournamentId
        self.gameIds = _gameIds
        self.playerIds = _playerIds
    def to_dict(self):
        return ({"tournamentId": self.tournamentId, "gameIds": self.gameIds, "playerIds": self.playerIds })

def setup():
    global Contract
    global w3
    compiled = json.load(open("/artifacts/contracts/GameResults.sol/GameResults.json", "r"))
    abi = compiled["abi"]
    bytecode = compiled["bytecode"]
    w3 = Web3(Web3.HTTPProvider('http://hardhat:8545'))
    w3.eth.default_account = w3.eth.accounts[0]
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = Contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    Contract = w3.eth.contract(address=tx_receipt.contractAddress,abi=abi)
    with open("ethereum.json", "w") as outfile:
        json.dump({"address": tx_receipt.contractAddress, "abi": abi}, outfile)

def _getContract():
    global Contract
    global w3
    if w3 is None:
        w3 = Web3(Web3.HTTPProvider('http://hardhat:8545'))
    with open('ethereum.json', 'r') as infile:
        json_object = json.load(infile)
    if "abi" in json_object and "address" in json_object:
        Contract = w3.eth.contract(address=json_object["address"],abi=json_object["abi"])
    else:
        raise Exception("Contract has not been initialized. Call setup() first.")

#Game function
##Setter
def addGame(_playerIds, _score, _gameType, _startTime, _endTime):
    global Contract
    global w3
    if Contract is None:
        _getContract()
    for id in _playerIds:
        exists = User.objects.filter(pk=id).exists()
        if not exists:
            raise Exception(f"User {id} doesn't exist")
    tx_hash = Contract.functions.addGame(_playerIds, _score, _gameType, _startTime, _endTime).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logs = Contract.events.GameAdded().process_receipt(tx_receipt)
    gameId = logs[0]['args']['gameId']
    return gameId
##Getter
def getGameById(index):
    global Contract
    if Contract is None:
        _getContract()
    gameObject = Contract.functions.getGameById(index).call()
    return Game(gameObject[0], gameObject[1], gameObject[2], gameObject[3], gameObject[4], gameObject[5])

def getGamesByPlayer(playerId):
    global Contract
    if Contract is None:
        _getContract()
    gameObject = Contract.functions.getGamesByPlayer(playerId).call()
    # logger.debug(gameObject)
    game = [Game(t[0], t[1], t[2], t[3], t[4], t[5]) for t in gameObject]
    return game

def getGamesNumber():
    global Contract
    if Contract is None:
        _getContract()
    return Contract.functions.getGamesNumber().call()

#Tournament function
##Setter
def addTournament(_gameIds, _playerIds):
    global Contract
    if Contract is None:
        _getContract()
    tx_hash = Contract.functions.addTournament(_gameIds, _playerIds).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    logs = Contract.events.TournamentAdded().process_receipt(tx_receipt)
    tournamentId = logs[0]['args']['tournamentId']
    return tournamentId
##Getter
def getTournamentById(id):  
    global Contract
    if Contract is None:
        _getContract()
    tournament = Contract.functions.getTournamentById(id).call()
    return {"tournamentId": tournament[0], "gamesId": tournament[1], "playersId": tournament[2]}

def getAllTournaments():
    global Contract
    if Contract is None:
        _getContract()
    tournaments = Contract.functions.getAllTournaments().call()
    return [Tournament(t[0], t[1], t[2]) for t in tournaments]

def getTournamentByPlayer(id):
    global Contract
    if Contract is None:
        _getContract()
    # logger.debug(f" {id} ")
    tournaments = Contract.functions.getTournamentByPlayer(id).call()
    return [Tournament(t[0], t[1], t[2]) for t in tournaments]
