from computable.contracts.deployed import Deployed

class Investing(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'investing.abi')

    def get_investment_price(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getInvestmentPrice')}, opts)
        return self.deployed.functions.getInvestmentPrice().call(opts)

    def invest(self, offer, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('invest')}, opts)
        return self.deployed.functions.invest(offer).transact(opts)

    def get_divestment_proceeds(sef, addr, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getDivestmentProceeds')}, opts)
        return self.deployed.functions.getDivestmentProceeds(addr).call(opts)

    def divest():
        opts = self.assign_transact_opts({'gas': self.get_gas('divest')}, opts)
        return self.deployed.functions.divest().transact(opts)
