import pytest
import web3
from web3 import Web3
from computable.helpers.transaction import call

def test_deploy(reserve):
    assert len(reserve.account) == 42
    assert len(reserve.address) == 42
    assert reserve.account != reserve.address

def test_get_withdrawal_proceeds(reserve):
    proceeds = call(reserve.get_withdrawal_proceeds(reserve.account))
    assert proceeds == 0

def test_withdraw(reserve):
    _ = call(reserve.withdraw())
    proceeds = call(reserve.get_withdrawal_proceeds(reserve.account))
    assert proceeds == 0
