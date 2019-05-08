import pytest
import web3
from web3 import Web3


def test_deploy(ether_token):
    assert len(ether_token.account) == 42
    assert len(ether_token.address) == 42
    assert ether_token.account != ether_token.address

def test_initial_balance(ether_token):
    owner_bal = ether_token.balanceOf(ether_token.account)
    assert owner_bal == Web3.toWei(1, 'ether')

# NOTE: Testing the ERC20 methods in EtherToken in addition to its additional methods
def test_approve_and_allowance(w3, ether_token):
    spender = w3.eth.accounts[1]
    # passing empty opts assures all defaults are used
    tx = ether_token.approve(spender, Web3.toWei(1, 'gwei'), {})
    allowed = ether_token.allowance(ether_token.account, w3.eth.accounts[1])
    assert allowed == Web3.toWei(1, 'gwei')
    # check the event
    rct = w3.eth.getTransactionReceipt(tx)
    logs = ether_token.deployed.events.Approval().processReceipt(rct)
    assert logs[0]['args']['amount'] == Web3.toWei(1, 'gwei')

def test_decrease_approval(w3, ether_token):
    spender = w3.eth.accounts[1]
    old_allowed = ether_token.allowance(ether_token.account, w3.eth.accounts[1])
    ether_token.decrease_approval(spender, Web3.toWei(1, 'mwei'), {})
    new_allowed = ether_token.allowance(ether_token.account, w3.eth.accounts[1])
    assert new_allowed == old_allowed - Web3.toWei(1, 'mwei')

def test_increase_approval(w3, ether_token):
    spender = w3.eth.accounts[1]
    old_allowed = ether_token.allowance(ether_token.account, w3.eth.accounts[1])
    ether_token.increase_approval(spender, Web3.toWei(1, 'kwei'), {})
    new_allowed = ether_token.allowance(ether_token.account, w3.eth.accounts[1])
    assert new_allowed == old_allowed + Web3.toWei(1, 'kwei')

def test_deposit(w3, ether_token):
    user = w3.eth.accounts[2]
    user_bal = ether_token.balanceOf(user)
    assert user_bal == 0
    # in normal use cases the user's account would be set, but here we'll just send it
    ether_token.deposit(Web3.toWei(1, 'gwei'), {'from': user})
    new_user_bal = ether_token.balanceOf(user)
    assert new_user_bal == Web3.toWei(1, 'gwei')

def test_total_supply(ether_token):
    supply = ether_token.total_supply()
    # don't care what it is, just care it's there
    assert supply > 0

def test_transfer(w3, ether_token):
    user = w3.eth.accounts[3]
    user_bal = ether_token.balanceOf(user)
    assert user_bal == 0
    owner_bal = ether_token.balanceOf(ether_token.account)
    # the default account is the initial balance holder here, so that works
    tx = ether_token.transfer(user, Web3.toWei(1, 'gwei'), {})
    new_user_bal = ether_token.balanceOf(user)
    new_owner_bal = ether_token.balanceOf(ether_token.account)
    assert new_user_bal == Web3.toWei(1, 'gwei')
    assert new_owner_bal == owner_bal - Web3.toWei(1, 'gwei')
    # event published...
    rct = w3.eth.getTransactionReceipt(tx)
    logs = ether_token.deployed.events.Transfer().processReceipt(rct)
    assert logs[0]['args']['amount'] == Web3.toWei(1, 'gwei')

def test_transfer_from(w3, ether_token):
    user = w3.eth.accounts[2]
    user_bal = ether_token.balanceOf(user)
    owner_bal = ether_token.balanceOf(ether_token.account)
    amt = Web3.toWei(1, 'mwei')
    # this user needs to approve the 'spender' (the owner in this test case)
    ether_token.approve(ether_token.account, amt, {'from': user})
    # with the allowance, that acct may transfer.
    ether_token.transfer_from(user, ether_token.account, amt, {})
    new_user_bal = ether_token.balanceOf(user)
    new_owner_bal = ether_token.balanceOf(ether_token.account)
    assert new_user_bal == user_bal - amt
    assert new_owner_bal == owner_bal + amt
    # should have 'zeroed' the allowance
    allowed = ether_token.allowance(user, ether_token.account)

def test_withdraw(w3, ether_token):
    user = w3.eth.accounts[2]
    user_bal = ether_token.balanceOf(user)
    tx = ether_token.withdraw(user_bal, {'from': user})
    new_user_bal = ether_token.balanceOf(user)
    assert new_user_bal == 0
    rct = w3.eth.getTransactionReceipt(tx)
    logs = ether_token.deployed.events.Withdraw().processReceipt(rct)
    assert logs[0]['args']['to'] == user
    assert logs[0]['args']['amount'] == user_bal
