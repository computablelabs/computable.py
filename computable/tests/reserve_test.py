import pytest
import web3
from web3 import Web3
from computable.helpers.transaction import call, transact

def test_deploy(reserve):
    assert len(reserve.account) == 42
    assert len(reserve.address) == 42
    assert reserve.account != reserve.address

def test_get_withdrawal_proceeds(reserve):
    proceeds = call(reserve.get_withdrawal_proceeds(reserve.account))
    assert proceeds == 0

def test_get_support_price(reserve):
    support_price = call(reserve.get_support_price())
    assert support_price == Web3.toWei(1, 'microether')

def test_support(w3, ether_token, market_token, reserve, listing):
    # Set market token privileges before this test
    priv = call(market_token.has_privilege(reserve.address))
    # May have been set previously
    if priv == False:
        tx = transact(market_token.set_privileged(reserve.address,
            listing.address))
        # wait for this to be mined
        rct = w3.eth.waitForTransactionReceipt(tx)
        # Check mining succeeded
        assert rct['status'] == 1
        priv = call(market_token.has_privilege(reserve.address))
        assert priv == True

    user = w3.eth.accounts[2]
    user_bal = call(ether_token.balance_of(user))
    assert user_bal == 0

    tx = transact(ether_token.deposit(
        Web3.toWei(1, 'ether'), {'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    new_user_bal = call(ether_token.balance_of(user))
    assert new_user_bal == Web3.toWei(1, 'ether')
    assert rct['status'] == 1

    old_allowance = call(ether_token.allowance(user, reserve.address))
    assert old_allowance == 0
    tx= transact(ether_token.approve(reserve.address, Web3.toWei(1, 'ether'), opts={'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    new_allowance = call(ether_token.allowance(user, reserve.address))
    assert new_allowance == Web3.toWei(1, 'ether')

    # Perform pre-checks for support 
    support_price = call(reserve.get_support_price())
    assert new_user_bal >= support_price
    assert new_allowance >= new_user_bal
    minted = (new_user_bal // support_price) * 10**9
    assert minted == 10**6 * Web3.toWei(1, 'gwei')
    priv = call(market_token.has_privilege(reserve.address))
    assert priv == True
    total_supply = call(market_token.total_supply())
    assert total_supply == Web3.toWei(2, 'ether')

    # Call support
    tx = transact(reserve.support(new_user_bal, opts={'gas': 1000000, 'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    logs = reserve.deployed.events.Supported().processReceipt(rct)
    cmt_user_bal = call(market_token.balance_of(user))
    assert cmt_user_bal == Web3.toWei(1, 'milliether')
    new_supply = call(market_token.total_supply())
    assert new_supply == total_supply + cmt_user_bal

def test_withdraw(w3, ether_token, market_token, reserve, listing):
    # Set market token privileges before this test
    priv = call(market_token.has_privilege(reserve.address))
    # It's possible the privilege may have been set already
    if priv == False:
        tx = transact(market_token.set_privileged(reserve.address,
            listing.address))
        # wait for this to be mined
        rct = w3.eth.waitForTransactionReceipt(tx)
        # Check mining succeeded
        assert rct['status'] == 1
        priv = call(market_token.has_privilege(reserve.address))
        assert priv == True
    # Use a new user
    user = w3.eth.accounts[3]
    tx = transact(ether_token.deposit(
        Web3.toWei(1, 'ether'), {'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    new_user_bal = call(ether_token.balance_of(user))
    assert new_user_bal == Web3.toWei(1, 'ether')

    # Approve the spend
    tx= transact(ether_token.approve(reserve.address, Web3.toWei(1, 'ether'), opts={'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1

    # Call support
    tx = transact(reserve.support(new_user_bal, opts={'gas': 1000000, 'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    cmt_user_bal = call(market_token.balance_of(user))
    # This is around one milliether, but not quite due to spread
    assert cmt_user_bal > 0 

    # Call withdraw 
    tx = transact(reserve.withdraw(opts={'gas': 1000000, 'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    cmt_user_bal = call(market_token.balance_of(user))
    # This should be 0 
    assert cmt_user_bal == 0 
    cet_user_bal = call(ether_token.balance_of(user))
    # Should be a little under 1 eth
    assert cet_user_bal > 0
