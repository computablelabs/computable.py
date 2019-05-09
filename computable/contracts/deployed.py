import os
import json
from computable.contracts.constants import GAS, GAS_PRICE


class Deployed:
    def __init__(self, acct):
        """
        @param acct Etherum address to use for transactions performed by this
        class instance
        """
        self.account = acct

    def assign_transact_opts(self, src, opts=None):
        """
        @param src Dict which will be returned after being hydrated with any
        passed in params or defaults
        @param opts Optional dict which may contain any number of transact opts.
        If not passed, the src object is simply returned
        """
        if opts is not None:
            if 'from' not in opts:
                opts['from'] = self.account
            if 'gas' not in opts:
                opts['gas'] = GAS
            if 'gas_price' not in opts:
                opts['gas_price'] = GAS_PRICE
            opts.update(src)
            return opts
        else:
            return src

    def at(self, w3, address, filename):
        """
        @param w3 An instance of Web3
        @param address EVM address of a deployed contract
        @param filename Name (with extension) of an abi file to read.
        NOTE: We expect the file to be read to be a sibling to this file (same dir)
        """
        abi = None
        path = os.path.join(os.path.dirname(__file__), filename)
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
