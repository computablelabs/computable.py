import os
import json
from computable.contracts.constants import GAS_PRICE, MIN_GAS, GAS_BUFFER


class Deployed:
    def __init__(self, acct):
        """
        @param acct Etherum address to use for transactions performed by this
        class instance
        """
        self.account = acct

    def assign_transact_opts(self, src, opts=None):
        """
        @param src Dict containing any class hydrated transact opts
        @param opts Optional dict containing any user-supplied transact opts
        """
        if opts is not None:
            # allow a more pythonic gas_price than all this mixed case bullshit
            if 'gas_price' in opts:
                src['gasPrice'] = opts['gas_price']
                del opts['gas_price']
                # TODO are there any other 'transactOpts' we'd like to snake_case?
            src.update(opts)

        if 'from' not in src:
            src['from'] = self.account
        if 'gasPrice' not in src:
            src['gasPrice'] = GAS_PRICE

        return src

    def at(self, w3, address, filename):
        """
        @param w3 An instance of Web3
        @param address EVM address of a deployed contract
        @param filename Name (with extension) of an abi file to read.
        """
        abi = None
        path = os.path.join(os.path.dirname(__file__), filename, '%s.abi'%(filename))
        with open(path) as f:
            abi = json.loads(f.read())
        if abi is None:
            raise ValueError('ABI json file not loaded')
        c = w3.eth.contract(
            address=address,
            abi=abi
            )
        # we'll use the full contract object in our HOCs
        self.deployed = c
        # hoist address for easy access
        self.address = address
        # remember the abi so we can fetch gas prices from it
        self.abi = abi

    def get_gas(self, method):
        """
        Given the name of a method on this class, fetch the gas cost approximated by the abi.
        NOTE: If no gas is found we will return the value for the constant GAS
        """
        gas = MIN_GAS
        for o in self.abi:
            if 'name' in o and o['name'] == method:
                gas = o['gas']
                break
        return gas + GAS_BUFFER
