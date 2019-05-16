import pytest
import web3
from web3 import Web3

def test_deploy(datatrust):
    assert len(datatrust.account) == 42
    assert len(datatrust.address) == 42
    assert datatrust.account != datatrust.address
