from computable.contracts.erc20 import ERC20

class MarketToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'markettoken')

    def set_privileged(self, reserve, listing, opts=None):
        """
        @param listing Address
        @param reserve Address
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setPrivileged')}, opts)
        return self.deployed.functions.setPrivileged(reserve, listing), opts

    def get_privileged(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getPrivileged')}, opts)
        return self.deployed.functions.getPrivileged(), opts

    def has_privilege(self, addr, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('hasPrivilege')}, opts)
        return self.deployed.functions.hasPrivilege(addr), opts
