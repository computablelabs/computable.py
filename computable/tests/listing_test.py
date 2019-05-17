import pytest
import web3
from web3 import Web3

def test_deploy(listing):
    assert len(listing.account) == 42
    assert len(listing.address) == 42
    assert listing.account != listing.address
