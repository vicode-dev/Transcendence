from web3 import Web3
import json
Contract = None
w3 = None
def test():
    w3 = Web3(Web3.HTTPProvider('http://hardhat:8545'))
    if w3.is_connected():
        return "Connected to Ethereum network"
    else:
        return "Failed to connect" 

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
    print("all setup")

def addGameResult(_gameId, _playerIds, _score, _duration, _startTime, _endTime):
    global Contract
    global w3
    if Contract is None:
        raise Exception("Contract has not been initialized. Call setup() first.")
    tx_hash = Contract.functions.addGameResult(_gameId, _playerIds, _score, _duration, _startTime, _endTime).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

def getGameResult(index):
    global Contract
    if Contract is None:
        raise Exception("Contract has not been initialized. Call setup() first.")
    return Contract.functions.getGameResult(index).call()

def getGameNumber():
    global Contract
    if Contract is None:
        raise Exception("Contract has not been initialized. Call setup() first.")
    return Contract.functions.getTotalResults().call()