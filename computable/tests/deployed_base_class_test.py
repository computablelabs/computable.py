import pytest
from web3 import Web3
from computable.contracts.deployed import Deployed
from computable.contracts.constants import GAS, GAS_PRICE

@pytest.fixture(scope='module')
def base_class(w3):
    base = Deployed(w3.eth.defaultAccount)
    return base

def test_assign_transact_opts_empty(base_class):
    defaults = base_class.assign_transact_opts({}, {})
    assert defaults['from'] == base_class.account
    assert defaults['gas'] == GAS
    assert defaults['gas_price'] == GAS_PRICE
    assert 'value' not in defaults

def test_assign_transact_opts(base_class):
    opts = base_class.assign_transact_opts({'value': Web3.toWei(1, 'gwei')}, {})
    assert opts['from'] == base_class.account
    assert opts['value'] == Web3.toWei(1, 'gwei')

def test_assign_transact_opts_pass_thru(base_class):
    noop = base_class.assign_transact_opts({'foo': 'bar'})
    assert len(noop.keys()) == 1
