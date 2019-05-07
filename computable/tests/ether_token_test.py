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
