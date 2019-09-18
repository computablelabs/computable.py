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
    print("support_price")
    print(support_price)
    assert support_price == Web3.toWei(1, 'microether')

def test_support(w3, ether_token, market_token, reserve, listing):
    # Set market token privileges before this test
    priv = call(market_token.has_privilege(reserve.address))
    assert priv == False
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

    # trying to manually perform support steps... 
    support_price = call(reserve.get_support_price())
    print("new_user_bal, support_price")
    print(new_user_bal, support_price)
    assert new_user_bal >= support_price
    assert new_allowance >= new_user_bal
    minted = (new_user_bal // support_price) * 10**9
    assert minted == 10**6 * Web3.toWei(1, 'gwei')
    priv = call(market_token.has_privilege(reserve.address))
    assert priv == True
    print("priv")
    print(priv)
    old_rsrv_cmt_bal = call(market_token.balance_of(reserve.address))
    print("old_rsrv_cmt_bal")
    print(old_rsrv_cmt_bal)
    old_user_cmt_bal = call(market_token.balance_of(reserve.address))
    print("old_user_cmt_bal")
    print(old_user_cmt_bal)
    tx = transact(reserve.support(new_user_bal, opts={'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    print("rct")
    print(rct)
    assert rct['status'] == 1
    assert 0 == 1
    #for e in reserve.deployed.events: print(e)
    #print("reserve.deployed.events.Supported()")
    #print(reserve.deployed.events.Supported())
    #logs = reserve.deployed.events.Supported().processReceipt(rct)
    #print("logs")
    #print(logs)

    #rsv_cmt_balance = call(market_token.balance_of(reserve.address))
    #print("rsv_cmt_balance")
    #print(rsv_cmt_balance)
    #cmt_balance = call(market_token.balance_of(user))
    #print("cmt_balance")
    #print(cmt_balance)
    #assert cmt_balance == 0
