import pytest
import web3
from web3 import Web3


def test_deploy(parameterizer):
    assert len(parameterizer.account) == 42
    assert len(parameterizer.address) == 42
    assert parameterizer.account != parameterizer.address
