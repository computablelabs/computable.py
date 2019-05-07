import os
import json
from computable.contracts.deployed import Deployed

class EtherToken(Deployed):
    def at(self, w3, address):
        abi = None
        path = os.path.join(os.path.dirname(__file__), 'ethertoken.abi')
        with open(path) as f:
            abi = json.loads(f.read())
        if abi is not None:
            super().at(w3, {'address': address, 'abi': abi})
        else:
            raise ValueError('ABI json file not loaded')

    def allowance(self, owner, spender):
        return self.deployed.allowance(owner, spender)

    def approve(self, spender, amount, opts):
        opts = self.assign_transact_opts({}, opts)
        self.deployed.approve(spender, amount, transact=opts)

    def balanceOf(self, owner):
        return self.deployed.balanceOf(owner)
