from computable.contracts.erc20 import ERC20

class MarketToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'markettoken.abi')

    def set_privileged(self, listing, reserve, opts=None):
        """
        @param listing Address
        @param reserve Address
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setPrivileged')}, opts)
        return self.deployed.functions.setPrivileged(listing, reserve), opts

    def get_privileged(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getPrivileged')}, opts)
        return self.deployed.functions.getPrivileged(), opts

    def has_privilege(self, addr, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('hasPrivilege')}, opts)
        return self.deployed.functions.hasPrivilege(addr), opts

    def get_decimals(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('decimals')}, opts)
        return self.deployed.functions.decimals(), opts

    def get_symbol(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('symbol')}, opts)
        return self.deployed.functions.symbol(), opts
