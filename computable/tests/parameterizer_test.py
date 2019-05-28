import pytest
import web3
from web3 import Web3
from computable.contracts.constants import SPREAD
from computable.helpers.transaction import call, transact


def test_deploy(parameterizer):
    assert len(parameterizer.account) == 42
    assert len(parameterizer.address) == 42
    assert parameterizer.account != parameterizer.address

def test_get_be_pay(parameterizer_opts, parameterizer):
    pay = call(parameterizer.get_backend_payment())
    assert pay == parameterizer_opts['backend_payment']

def test_get_mk_pay(parameterizer_opts, parameterizer):
    pay = call(parameterizer.get_maker_payment())
    assert pay == parameterizer_opts['maker_payment']

def test_get_rs_pay(parameterizer_opts, parameterizer):
    be = call(parameterizer.get_backend_payment())
    mk = call(parameterizer.get_maker_payment())
    pay = call(parameterizer.get_reserve_payment())
    assert pay == 100 - be - mk

def test_get_cost_per(parameterizer_opts, parameterizer):
    cost = call(parameterizer.get_cost_per_byte())
    assert cost == parameterizer_opts['cost_per_byte']

def test_get_stake(parameterizer_opts, parameterizer):
    stake = call(parameterizer.get_stake())
    assert stake == parameterizer_opts['stake']

def test_get_price_floor(parameterizer_opts, parameterizer):
    price = call(parameterizer.get_price_floor())
    assert price == parameterizer_opts['price_floor']

def test_get_price_floor(parameterizer_opts, parameterizer):
    price = call(parameterizer.get_price_floor())
    assert price == parameterizer_opts['price_floor']

def test_get_hash(parameterizer):
    hash = call(parameterizer.get_hash(SPREAD, 115))
    other_hash = Web3.soliditySha3(['uint256', 'uint256'], [SPREAD, 115])
    assert hash == other_hash

def test_get_spread(parameterizer_opts, parameterizer):
    spread = call(parameterizer.get_spread())
    assert spread == parameterizer_opts['spread']


def test_get_list_reward(parameterizer_opts, parameterizer):
    reward = call(parameterizer.get_list_reward())
    assert reward == parameterizer_opts['list_reward']

def test_get_plurality(parameterizer_opts, parameterizer):
    pl = call(parameterizer.get_plurality())
    assert pl == parameterizer_opts['plurality']


def test_get_vote_by(parameterizer_opts, parameterizer):
    end = call(parameterizer.get_vote_by())
    assert end == parameterizer_opts['vote_by']
