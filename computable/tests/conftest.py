import os
import json
import pytest
import web3
from web3 import Web3
from computable.contracts.ether_token import EtherToken
from computable.contracts.market_token import MarketToken


@pytest.fixture(scope='module')
def w3():
    instance = Web3(Web3.EthereumTesterProvider())
    instance.eth.defaultAccount = instance.eth.accounts[0] # our test 'owner' account
    return instance

@pytest.fixture(scope='module')
def ether_token_opts():
    return {'init_bal': Web3.toWei(1, 'ether')}

@pytest.fixture(scope='module')
def ether_token(w3, ether_token_opts):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'ethertoken.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'ethertoken.bin')) as f:
        bc = f.read()
    token = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = token.constructor(w3.eth.defaultAccount,
        ether_token_opts['init_bal']).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    ether_token = EtherToken(w3.eth.defaultAccount)
    ether_token.at(w3, tx_rcpt['contractAddress'])
    return ether_token

@pytest.fixture(scope='module')
def market_token_opts():
    return {'init_bal': Web3.toWei(2, 'ether')}

@pytest.fixture(scope='module')
def market_token(w3, market_token_opts):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'markettoken.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'markettoken.bin')) as f:
        bc = f.read()
    token = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = token.constructor(w3.eth.defaultAccount,
        market_token_opts['init_bal']).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    market_token = MarketToken(w3.eth.defaultAccount)
    market_token.at(w3, tx_rcpt['contractAddress'])
    return market_token
