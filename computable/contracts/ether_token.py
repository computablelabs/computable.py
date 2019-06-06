from computable.contracts.erc20 import ERC20

class EtherToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'ethertoken.abi')

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

    def get_decimals(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('decimals')}, opts)
        return self.deployed.functions.decimals(), opts

    def get_symbol(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('symbol')}, opts)
        return self.deployed.functions.symbol(), opts
