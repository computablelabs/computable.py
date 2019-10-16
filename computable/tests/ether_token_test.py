import pytest
import web3
from web3 import Web3
from computable.contracts.constants import GAS_BUFFER
from computable.helpers.transaction import call, transact

def test_deploy(ether_token):
    assert len(ether_token.account) == 42
    assert len(ether_token.address) == 42
    assert ether_token.account != ether_token.address

# NOTE: Testing the ERC20 methods in EtherToken in addition to its additional methods
def test_approve_and_allowance(w3, ether_token):
    # exact gas amounts are known
    gas = ether_token.get_gas('approve')
    assert gas == 37763 + GAS_BUFFER # looked up manually in the abi
    spender = w3.eth.accounts[1]
    # passing empty opts assures all defaults are used
    tx = transact(ether_token.approve(spender, Web3.toWei(1, 'gwei')))
    allowed = call(ether_token.allowance(ether_token.account, w3.eth.accounts[1]))
    assert allowed == Web3.toWei(1, 'gwei')
    # check the event
    rct = w3.eth.getTransactionReceipt(tx)
    logs = ether_token.deployed.events.Approval().processReceipt(rct)
    assert logs[0]['args']['amount'] == Web3.toWei(1, 'gwei')

def test_decrease_allowance(w3, ether_token):
    spender = w3.eth.accounts[1]
    old_allowed = call(ether_token.allowance(ether_token.account, w3.eth.accounts[1]))
    transact(ether_token.decrease_allowance(spender, Web3.toWei(1, 'mwei')))
    new_allowed = call(ether_token.allowance(ether_token.account, w3.eth.accounts[1]))
    assert new_allowed == old_allowed - Web3.toWei(1, 'mwei')

def test_increase_allowance(w3, ether_token):
    spender = w3.eth.accounts[1]
    old_allowed = call(ether_token.allowance(ether_token.account, w3.eth.accounts[1]))
    transact(ether_token.increase_allowance(spender, Web3.toWei(1, 'kwei')))
    new_allowed = call(ether_token.allowance(ether_token.account, w3.eth.accounts[1]))
    assert new_allowed == old_allowed + Web3.toWei(1, 'kwei')

def test_deposit(w3, ether_token):
    user = w3.eth.accounts[2]
    user_bal = call(ether_token.balance_of(user))
    assert user_bal == 0
    # in normal use cases the user's account would be set, but here we'll just send it
    transact(ether_token.deposit(Web3.toWei(1, 'gwei'), {'from': user}))
    new_user_bal = call(ether_token.balance_of(user))
    assert new_user_bal == Web3.toWei(1, 'gwei')

def test_total_supply(ether_token):
    supply = call(ether_token.total_supply())
    # don't care what it is, just care it's there
    assert supply > 0

def test_transfer(w3, ether_token):
    user = w3.eth.accounts[3]
    other = w3.eth.accounts[4]
    user_bal = call(ether_token.balance_of(user))
    other_bal = call(ether_token.balance_of(other))
    assert user_bal == 0
    assert other_bal == 0
    # Let's deposit 1 ether token in user's account 
    transact(ether_token.deposit(Web3.toWei(1, 'gwei'), {'from': user}))
    # Let's send this to other 
    tx = transact(ether_token.transfer(other, Web3.toWei(1, 'gwei'), {'from': user}))
    new_user_bal = call(ether_token.balance_of(user))
    new_other_bal = call(ether_token.balance_of(other))
    assert new_user_bal == 0 
    assert new_other_bal == Web3.toWei(1, 'gwei')
    # event published...
    rct = w3.eth.getTransactionReceipt(tx)
    logs = ether_token.deployed.events.Transfer().processReceipt(rct)
    assert logs[0]['args']['amount'] == Web3.toWei(1, 'gwei')

def test_transfer_from(w3, ether_token):
    user = w3.eth.accounts[2]
    user_bal = call(ether_token.balance_of(user))
    owner_bal = call(ether_token.balance_of(ether_token.account))
    amt = Web3.toWei(1, 'mwei')
    # this user needs to approve the 'spender' (the owner in this test case)
    transact(ether_token.approve(ether_token.account, amt, {'from': user}))
    # with the allowance, that acct may transfer.
    transact(ether_token.transfer_from(user, ether_token.account, amt))
    new_user_bal = call(ether_token.balance_of(user))
    new_owner_bal = call(ether_token.balance_of(ether_token.account))
    assert new_user_bal == user_bal - amt
    assert new_owner_bal == owner_bal + amt
    # should have 'zeroed' the allowance
    allowed = call(ether_token.allowance(user, ether_token.account))

def test_withdraw(w3, ether_token):
    user = w3.eth.accounts[2]
    user_bal = call(ether_token.balance_of(user))
    tx = transact(ether_token.withdraw(user_bal, {'from': user}))
    new_user_bal = call(ether_token.balance_of(user))
    assert new_user_bal == 0
    rct = w3.eth.getTransactionReceipt(tx)
    logs = ether_token.deployed.events.Withdrawn().processReceipt(rct)
    assert logs[0]['args']['to'] == user
    assert logs[0]['args']['amount'] == user_bal

def test_decimals(ether_token):
    decimals = call(ether_token.get_decimals())
    assert decimals == 18

def test_symbol(ether_token):
    symbol = call(ether_token.get_symbol())
    assert symbol == "CET"
