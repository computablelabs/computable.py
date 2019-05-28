import pytest
import web3
from web3 import Web3
from computable.helpers.account import lock, unlock

# While we don't recommend using the lock/unlock pattern, the helpers should still work
def test_lock_account(w3, user):
    assert lock(w3, user) == True

def test_unlock(w3, passphrase, user):
    assert unlock(w3, 'not-the-phrase', user) == False
    assert unlock(w3, passphrase, user) == True
