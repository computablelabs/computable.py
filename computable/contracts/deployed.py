from web3.contract import ConciseContract
from computable.contracts.constants import GAS, GAS_PRICE


class Deployed:
    def __init__(self, acct):
        """
        @param acct Etherum address to use for transactions performed by this
        class instance
        """
        self.account = acct

    def assign_transact_opts(self, src, opts):
        """
        @param src Dict which will be returned after being hydrated with any
        passed in params or defaults
        @param opts Dict which may contain any number of transact opts
        """
        if opts is not None:
            if opts['from'] is None:
                opts['from'] = self.account
            if opts['gas'] is None:
                opts['gas'] = GAS
            if opts['gas_price'] is None:
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
        # we'll use the more succinct syntax of the concise class
        self.deployed = ConciseContract(c)
        # hoist address for easy access
        self.address = params['address']

    def require_account(self, opts):
        """
        @param opts Dict to check for the presence of an address
        @return An Ethereum address
        """
        return opts['from'] or self.account
