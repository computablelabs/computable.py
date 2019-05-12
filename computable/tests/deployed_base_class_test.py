import pytest
from web3 import Web3
from computable.contracts.deployed import Deployed
from computable.contracts.constants import GAS_PRICE

@pytest.fixture(scope='module')
def base_class(w3):
    base = Deployed(w3.eth.defaultAccount)
    return base

def test_assign_transact_opts_empty(base_class):
    defaults = base_class.assign_transact_opts({})
    assert defaults['from'] == base_class.account
    assert defaults['gas_price'] == GAS_PRICE
    assert 'value' not in defaults

def test_assign_transact_opts(base_class):
    opts = base_class.assign_transact_opts({'value': Web3.toWei(1, 'gwei')})
    assert opts['from'] == base_class.account
    assert opts['value'] == Web3.toWei(1, 'gwei')

def test_assign_transact_opts_overwrite(base_class):
    opts = base_class.assign_transact_opts({'spam': 'eggs'}, {'spam': 'vikings'})
    assert opts['spam'] == 'vikings'
