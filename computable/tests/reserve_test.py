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

def test_support(w3, ether_token, reserve):
    user = w3.eth.accounts[2]
    user_bal = call(ether_token.balance_of(user))
    assert user_bal == 0

    transact(ether_token.deposit(
        Web3.toWei(1, 'ether'), {'from': user}))
    new_user_bal = call(ether_token.balance_of(user))
    assert new_user_bal == Web3.toWei(1, 'ether')

    support_price = call(reserve.get_support_price())
    assert new_user_bal >= support_price

    old_allowance = call(ether_token.allowance(user, reserve.address))
    assert old_allowance == 0

    transact(ether_token.increase_approval(reserve.address, Web3.toWei(1, 'ether'), opts={'from': user}))

    new_allowance = call(ether_token.allowance(user, reserve.address))
    assert new_allowance == Web3.toWei(1, 'ether')

    out = call(reserve.support(new_user_bal, opts={'from': user}))
    assert 0 == 1
    #_ = call(reserve.withdraw())
    #proceeds = call(reserve.get_withdrawal_proceeds(reserve.account))
    #assert proceeds == 0
