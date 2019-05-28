import pytest
import web3
from web3 import Web3
import computable.helpers.transaction as tx_helpers
from computable.helpers.account import lock
from computable.contracts.constants import GAS_PRICE

def test_send_some_eth(w3, user):
    """
    our created user account will need a balance in order to do anything
    """
    user_bal = w3.eth.getBalance(user)
    assert user_bal == 0
    tx = w3.eth.sendTransaction({
        'from': w3.eth.defaultAccount,
        'to': user,
        'gas': 121000,
        'gasPrice': GAS_PRICE,
        'value': Web3.toWei(1, 'finney')
        })
    rct = w3.eth.waitForTransactionReceipt(tx)
    new_user_bal = w3.eth.getBalance(user)
    assert new_user_bal == Web3.toWei(1, 'finney')

def test_send_some_ether_token(w3, user, ether_token):
    user_bal = tx_helpers.call(ether_token.balance_of(user))
    assert user_bal == 0
    tx = tx_helpers.transact(ether_token.transfer(user, Web3.toWei(1, 'gwei')))
    new_user_bal = tx_helpers.call(ether_token.balance_of(user))
    assert new_user_bal == Web3.toWei(1, 'gwei')

def test_build_sign_send_transaction(w3, pk, user, ether_token):
    """
    transactions may be broken apart into each individual step in order to facilitate various signing
    methods (like crypto sticks for instance)
    """
    lock(w3, user) # assure the account is locked
    other_user = w3.eth.accounts[1] # we'll send some tokens to this target
    other_user_bal = tx_helpers.call(ether_token.balance_of(other_user))
    assert other_user_bal == 0
    # all computable.py HOC methods return a tuple in the form: (tx, opts)
    tup = ether_token.transfer(other_user, Web3.toWei(1, 'kwei'), {'from': user})
    # these may be passed directly to build...
    built_tx = tx_helpers.build_transaction(w3, tup)
    assert built_tx['from'] == user
    # sign it
    signed_tx = tx_helpers.sign_transaction(w3, pk.to_bytes(), built_tx)
    assert signed_tx.hash is not None
    assert signed_tx.r is not None
    assert signed_tx.s is not None
    assert signed_tx.v is not None
    # a signed transaction can then be broadcast
    final_tx = tx_helpers.send_raw_transaction(w3, signed_tx)
    rct = w3.eth.waitForTransactionReceipt(final_tx)
    other_user_new_bal = tx_helpers.call(ether_token.balance_of(other_user))
    assert other_user_new_bal == Web3.toWei(1, 'kwei')

def test_send(w3, pk, user, ether_token):
    """
    we do provide an all-in-one convenience method for offline signing
    """
    other_user = w3.eth.accounts[2] # we'll send some tokens to this target
    other_user_bal = tx_helpers.call(ether_token.balance_of(other_user))
    assert other_user_bal == 0
    tx = tx_helpers.send(w3, pk.to_bytes(), ether_token.transfer(other_user, Web3.toWei(1, 'kwei'), {'from': user}))
    rct = w3.eth.waitForTransactionReceipt(tx)
    other_user_new_bal = tx_helpers.call(ether_token.balance_of(other_user))
    assert other_user_new_bal == Web3.toWei(1, 'kwei')
