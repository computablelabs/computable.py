import pytest
import web3
from web3 import Web3

def test_deploy(investing):
    assert len(investing.account) == 42
    assert len(investing.address) == 42
    assert investing.account != investing.address
