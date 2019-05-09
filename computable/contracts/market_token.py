from computable.contracts.erc20 import ERC20

class MarketToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'markettoken.abi')

    def burn(self, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.burn(amount).transact(opts)

    def burn_all(self, address, opts):
        """
        NOTE: Callable only by a privileged address
        """
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.burnAll(address).transact(opts)

    def mint(self, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.mint(amount).transact(opts)
