from computable.contracts.deployed import Deployed

class ERC20(Deployed):
    def allowance(self, owner, spender, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('allowance')}, opts)
        return self.deployed.functions.allowance(owner, spender), opts

    def approve(self, spender, amount, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('approve')}, opts)
        return self.deployed.functions.approve(spender, amount), opts

    def balance_of(self, owner, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('balanceOf')}, opts)
        return self.deployed.functions.balanceOf(owner), opts

    def decrease_allowance(self, spender, amount, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('decreaseApproval')}, opts)
        return self.deployed.functions.decreaseAllowance(spender, amount), opts

    def increase_allowance(self, spender, amount, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('increaseApproval')}, opts)
        return self.deployed.functions.increaseAllowance(spender, amount), opts

    def total_supply(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('totalSupply')}, opts)
        return self.deployed.functions.totalSupply(), opts

    def transfer(self, to, amount, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('transfer')}, opts)
        return self.deployed.functions.transfer(to, amount), opts

    def transfer_from(self, source, to, amount, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('transferFrom')}, opts)
        return self.deployed.functions.transferFrom(source, to, amount), opts

    def get_decimals(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('decimals')}, opts)
        return self.deployed.functions.decimals(), opts

    def get_symbol(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('symbol')}, opts)
        return self.deployed.functions.symbol(), opts
