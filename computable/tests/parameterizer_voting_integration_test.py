import pytest
import web3
from web3 import Web3
from computable.contracts.constants import PLURALITY, REPARAM
from computable.helpers.transaction import call, transact

def test_set_privileged(w3, ether_token, voting, parameterizer, reserve,):
    # Check privilege set correctly 
    priv = call(voting.has_privilege(parameterizer.address))
    assert priv == True

def test_reparameterize(w3, ether_token, market_token, voting, parameterizer, reserve, listing):
    # Set market token privileges before this test
    priv = call(market_token.has_privilege(reserve.address))
    assert priv == True
 
    user = w3.eth.accounts[2]
    user_bal = call(ether_token.balance_of(user))
    assert user_bal == 0
 
    # Deposit ETH in EtherToken
    tx = transact(ether_token.deposit(
        Web3.toWei(10, 'ether'), {'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    new_user_bal = call(ether_token.balance_of(user))
    assert new_user_bal == Web3.toWei(10, 'ether')
    assert rct['status'] == 1
 
    # Approve the spend
    old_allowance = call(ether_token.allowance(user, reserve.address))
    assert old_allowance == 0
    tx= transact(ether_token.approve(reserve.address, Web3.toWei(10, 'ether'), opts={'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    new_allowance = call(ether_token.allowance(user, reserve.address))
    assert new_allowance == Web3.toWei(10, 'ether')
 
    # Perform pre-checks for support 
    support_price = call(reserve.get_support_price())
    assert new_user_bal >= support_price
    assert new_allowance >= new_user_bal
    minted = (new_user_bal // support_price) * 10**9
    assert minted == 10**7 * Web3.toWei(1, 'gwei')
    priv = call(market_token.has_privilege(reserve.address))
    assert priv == True
    total_supply = call(market_token.total_supply())
    assert total_supply == Web3.toWei(2, 'ether')
 
    # Call support
    tx = transact(reserve.support(new_user_bal, opts={'gas': 1000000, 'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    logs = reserve.deployed.events.Supported().processReceipt(rct)
    cmt_user_bal = call(market_token.balance_of(user))
    assert cmt_user_bal == Web3.toWei(10, 'milliether')
    new_supply = call(market_token.total_supply())
    assert new_supply == total_supply + cmt_user_bal

    # Approve the market token allowance
    old_mkt_allowance = call(market_token.allowance(user, voting.address))
    assert old_mkt_allowance == 0
    tx = transact(market_token.approve(voting.address, Web3.toWei(10, 'milliether'), opts={'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
    new_mkt_allowance = call(market_token.allowance(user, voting.address))
    assert new_mkt_allowance == Web3.toWei(10, 'milliether')

    stake = call(parameterizer.get_stake())
    print("stake")
    print(stake)
    assert stake <= new_mkt_allowance
    
    tx = transact(parameterizer.reparameterize(PLURALITY, 51, opts={'gas': 500000, 'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    assert rct['status'] == 1
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

def test_get_candidate(w3, voting, parameterizer):
    user = w3.eth.accounts[2]
    hash = call(parameterizer.get_hash(PLURALITY, 51))
    stake = call(parameterizer.get_stake())
    vote_by = call(parameterizer.get_vote_by())
    tup = call(voting.get_candidate(hash))
    assert tup[0] == REPARAM
    assert tup[1] == user
    assert tup[2] == stake
    # the p11r vote by is simply the delta, returned val is actual end date
    assert tup[3] > vote_by # should pass even at a 0 vote_by
    assert tup[4] == 0
    assert tup[5] == 0
