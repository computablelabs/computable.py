from computable.contracts.erc20 import ERC20

class EtherToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'ethertoken')

    def deposit(self, amount, opts=None):
        """
        @param amount An amount of ETH, in wei, sent as msg.value
        @param opts Transact Opts for this send type method
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('deposit'), 'value': amount}, opts)
        return self.deployed.functions.deposit(), opts

    def withdraw(self, amount, opts=None):
        """
        @param amount An amount of ETH, in wei, to withdraw from this contract
        by its owner
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('withdraw')}, opts)
        return self.deployed.functions.withdraw(amount), opts
