import pytest
import web3
from web3 import Web3

def test_deploy(reserve):
    assert len(reserve.account) == 42
    assert len(reserve.address) == 42
    assert reserve.account != reserve.address
