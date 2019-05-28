import pytest
import web3
from web3 import Web3
from computable.helpers.transaction import call

def test_deploy(market_token):
    assert len(market_token.account) == 42
    assert len(market_token.address) == 42
    assert market_token.account != market_token.address

def test_initial_balance(market_token):
    owner_bal = call(market_token.balance_of(market_token.account))
    assert owner_bal == Web3.toWei(2, 'ether')
