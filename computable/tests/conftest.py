import os
import json
import pytest
import web3
from web3 import Web3
from computable.contracts.constants import SECONDS_IN_A_DAY
from computable.contracts.ether_token import EtherToken
from computable.contracts.market_token import MarketToken
from computable.contracts.voting import Voting
from computable.contracts.parameterizer import Parameterizer
from computable.contracts.investing import Investing

@pytest.fixture(scope='module')
def test_provider():
    return Web3.EthereumTesterProvider()

@pytest.fixture(scope='module')
def w3(test_provider):
    instance = Web3(test_provider)
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
    t = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = t.constructor(w3.eth.defaultAccount,
        ether_token_opts['init_bal']).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    token = EtherToken(w3.eth.defaultAccount)
    token.at(w3, tx_rcpt['contractAddress'])
    return token

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
    t = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = t.constructor(w3.eth.defaultAccount,
        market_token_opts['init_bal']).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    token = MarketToken(w3.eth.defaultAccount)
    token.at(w3, tx_rcpt['contractAddress'])
    return token

@pytest.fixture(scope='module')
def voting(w3, market_token):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'voting.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'voting.bin')) as f:
        bc = f.read()
    v = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = v.constructor(market_token.address).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    vg = Voting(w3.eth.defaultAccount)
    vg.at(w3, tx_rcpt['contractAddress'])
    return vg

@pytest.fixture(scope='module')
def parameterizer_opts():
    return {
                'price_floor': Web3.toWei(1, 'szabo'),
                'spread': 110,
                'list_reward': Web3.toWei(250, 'szabo'),
                'stake': Web3.toWei(10, 'finney'),
                'vote_by': 100,
                'plurality': 50,
                'backend_payment': 25,
                'maker_payment': 25,
                'cost_per_byte': Web3.toWei(100, 'gwei')
            }

@pytest.fixture(scope='module')
def parameterizer(w3, voting, parameterizer_opts):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'parameterizer.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'parameterizer.bin')) as f:
        bc = f.read()
    p = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = p.constructor(
            voting.address,
            parameterizer_opts['price_floor'],
            parameterizer_opts['spread'],
            parameterizer_opts['list_reward'],
            parameterizer_opts['stake'],
            parameterizer_opts['vote_by'],
            parameterizer_opts['plurality'],
            parameterizer_opts['backend_payment'],
            parameterizer_opts['maker_payment'],
            parameterizer_opts['cost_per_byte']
            ).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    p11r = Parameterizer(w3.eth.defaultAccount)
    p11r.at(w3, tx_rcpt['contractAddress'])
    return p11r

@pytest.fixture(scope='module')
def investing(w3, ether_token, market_token, parameterizer):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'investing.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'investing.bin')) as f:
        bc = f.read()
    i = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = i.constructor(ether_token.address, market_token.address, 
            parameterizer.address).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    inv = Investing(w3.eth.defaultAccount)
    inv.at(w3, tx_rcpt['contractAddress'])
    return inv
