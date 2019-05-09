from computable.contracts.erc20 import ERC20

class EtherToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'ethertoken.abi')

    def deposit(self, amount, opts):
        """
        @param amount An amount of ETH, in wei, sent as msg.value
        """
        opts = self.assign_transact_opts({'value': amount}, opts)
        return self.deployed.functions.deposit().transact(opts)

    def withdraw(self, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.withdraw(amount).transact(opts)
