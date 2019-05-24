import pytest
import web3
from web3 import Web3
from computable.contracts.constants import PLURALITY, REPARAM
from computable.helpers.transaction import call, transact

def test_set_privileged(w3, voting, parameterizer):
    # we can set the real p11r address and 3 imposters for this test
    priv = call(voting.has_privilege(parameterizer.address))
    assert priv == False
    # voting acct is the owner address
    tx = transact(voting.set_privileged(parameterizer.address, w3.eth.accounts[7],
            w3.eth.accounts[8], w3.eth.accounts[9]))
    # wait for this to be mined
    rct = w3.eth.waitForTransactionReceipt(tx)
    priv = call(voting.has_privilege(parameterizer.address))
    assert priv == True

def test_reparameterize(w3, parameterizer):
    tx = transact(parameterizer.reparameterize(PLURALITY, 51))
    rct = w3.eth.waitForTransactionReceipt(tx)
    logs = parameterizer.deployed.events.ReparamProposed().processReceipt(rct)
    hash = call(parameterizer.get_hash(PLURALITY, 51))
    # should see an event with the calculated hash for those vals
    assert logs[0]['args']['hash'] == hash

def test_is_candidate(voting, parameterizer):
    hash = call(parameterizer.get_hash(PLURALITY, 51))
    is_can = call(voting.is_candidate(hash))
    assert is_can == True

def test_candidate_is(voting, parameterizer):
    hash = call(parameterizer.get_hash(PLURALITY, 51))
    can_is = call(voting.candidate_is(hash, REPARAM))
    assert can_is == True

def test_get_candidate(voting, parameterizer):
    hash = call(parameterizer.get_hash(PLURALITY, 51))
    stake = call(parameterizer.get_stake())
    vote_by = call(parameterizer.get_vote_by())
    tup = call(voting.get_candidate(hash))
    assert tup[0] == REPARAM
    assert tup[1] == parameterizer.account
    assert tup[2] == stake
    # the p11r vote by is simply the delta, returned val is actual end date
    assert tup[3] > vote_by # should pass even at a 0 vote_by
    assert tup[4] == 0
    assert tup[5] == 0
