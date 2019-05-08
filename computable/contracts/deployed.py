from web3.contract import ConciseContract
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

    def at(self, w3, params):
        """
        @param w3 An instance of Web3
        @param params Dict containing address and abi parameters
        """
        c = w3.eth.contract(
            address=params['address'],
            abi=params['abi']
            )
        # we'll use the full contract object in our HOCs
        self.deployed = c
        # hoist address for easy access
        self.address = params['address']
