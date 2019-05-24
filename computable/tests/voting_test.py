import pytest
import web3
from web3 import Web3
from computable.helpers.transaction import call

def test_deploy(voting):
    assert len(voting.account) == 42
    assert len(voting.address) == 42
    assert voting.account != voting.address

def test_is_candidate(voting):
    hash = Web3.sha3(text='nope')
    assert call(voting.is_candidate(hash)) == False

def test_candidate_is(voting):
    hash = Web3.sha3(text='stillnope')
    assert call(voting.candidate_is(hash, 1)) == False
