import os
import json
from computable.contracts.deployed import Deployed

class ERC20(Deployed):
    def allowance(self, owner, spender, opts=None):
        return self.deployed.functions.allowance(owner, spender).call(opts)

    def approve(self, spender, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.approve(spender, amount).transact(opts)

    def balanceOf(self, owner, opts=None):
        return self.deployed.functions.balanceOf(owner).call(opts)

    def decrease_approval(self, spender, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.decreaseApproval(spender, amount).transact(opts)

    def increase_approval(self, spender, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.increaseApproval(spender, amount).transact(opts)

    def total_supply(self, opts=None):
        return self.deployed.functions.totalSupply().call(opts)

    def transfer(self, to, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.transfer(to, amount).transact(opts)

    def transfer_from(self, source, to, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.transferFrom(source, to, amount).transact(opts)
