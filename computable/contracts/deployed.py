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
        # default the chain_id to None
        self.chain_id = None

    def assign_transact_opts(self, src, opts=None):
        """
        @param src Dict containing any class hydrated transact opts
        @param opts Optional dict containing any user-supplied transact opts
        """
        if 'from' not in src:
            src['from'] = self.account
        if 'gasPrice' not in src:
            src['gasPrice'] = GAS_PRICE
        if 'chainId' not in src:
            src['chainId'] = self.chain_id

        if opts is not None:
            src.update(opts)
        return src

    def at(self, w3, address, filename, chain_id=None):
        """
        @param w3 An instance of Web3
        @param address EVM address of a deployed contract
        @param filename Name (with extension) of an abi file to read.
        @param chain_id Identifier of the block chain `address` is on (or None)
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
        # remember the abi so we can fetch gas prices from it
        self.abi = abi
        # set the passed in chainId if present
        if chain_id is not None:
            self.chain_id = chain_id

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
