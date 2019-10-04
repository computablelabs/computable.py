from computable.contracts.deployed import Deployed

class Reserve(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'reserve')

    def get_support_price(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getSupportPrice')}, opts)
        return self.deployed.functions.getSupportPrice(), opts

    def support(self, offer, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('support')}, opts)
        return self.deployed.functions.support(offer), opts

    def get_withdrawal_proceeds(self, addr, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getWithdrawalProceeds')}, opts)
        return self.deployed.functions.getWithdrawalProceeds(addr), opts

    def withdraw(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('withdraw')}, opts)
        return self.deployed.functions.withdraw(), opts
