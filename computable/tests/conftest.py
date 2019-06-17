import os
import json
import pytest
import web3
from web3 import Web3
from eth_keys import keys
from computable.contracts import EtherToken
from computable.contracts import MarketToken
from computable.contracts import Voting
from computable.contracts import Parameterizer
from computable.contracts import Reserve
from computable.contracts import Datatrust
from computable.contracts import Listing

# Web3
@pytest.fixture(scope='module')
def test_provider():
    return Web3.EthereumTesterProvider()

@pytest.fixture(scope='module')
def w3(test_provider):
    instance = Web3(test_provider)
    instance.eth.defaultAccount = instance.eth.accounts[0] # our test 'owner' account
    return instance

# User (when the default, unlocked accounts will not suffice)
@pytest.fixture(scope='module')
def passphrase():
    return 'spam-eggs-vikings'

@pytest.fixture(scope='module')
def pk():
    return keys.PrivateKey(b'\x01' * 32)

@pytest.fixture(scope='module')
def user(w3, pk, passphrase):
    return w3.geth.personal.importRawKey(pk.to_hex(), passphrase)

# Contracts
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
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(w3.eth.defaultAccount,
        ether_token_opts['init_bal']).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    instance = EtherToken(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance

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
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(w3.eth.defaultAccount,
        market_token_opts['init_bal']).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    instance = MarketToken(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance

@pytest.fixture(scope='module')
def voting(w3, market_token):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'voting.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'voting.bin')) as f:
        bc = f.read()
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(market_token.address).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    instance = Voting(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance

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
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(
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
    instance = Parameterizer(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance

@pytest.fixture(scope='module')
def reserve(w3, ether_token, market_token, parameterizer):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'reserve.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'reserve.bin')) as f:
        bc = f.read()
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(ether_token.address, market_token.address,
            parameterizer.address).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    instance = Reserve(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance

@pytest.fixture(scope='module')
def datatrust(w3, ether_token, voting, parameterizer, reserve):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'datatrust.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'datatrust.bin')) as f:
        bc = f.read()
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(ether_token.address, voting.address,
            parameterizer.address, reserve.address).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    instance = Datatrust(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance

@pytest.fixture(scope='module')
def listing(w3, market_token, voting, parameterizer, datatrust, reserve):
    contract_path = os.path.join(os.path.dirname(__file__), os.pardir, 'contracts')
    with open(os.path.join(contract_path, 'listing.abi')) as f:
        abi = json.loads(f.read())
    with open(os.path.join(contract_path, 'listing.bin')) as f:
        bc = f.read()
    deployed = w3.eth.contract(abi=abi, bytecode=bc.rstrip('\n'))
    tx_hash = deployed.constructor(market_token.address, voting.address,
            parameterizer.address, datatrust.address, reserve.address).transact()
    tx_rcpt = w3.eth.waitForTransactionReceipt(tx_hash)
    instance = Listing(w3.eth.defaultAccount)
    instance.at(w3, tx_rcpt['contractAddress'])
    return instance
