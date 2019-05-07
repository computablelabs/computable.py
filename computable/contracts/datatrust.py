import json
from computable.contracts.deployed import Deployed


class Datatrust(Deployed):
    def at(self, w3, address):
        abi = None
        with open('datatrust.abi') as f:
            abi = json.loads(f.read())
        if abi is not None:
            super().at(w3, {'address': address, 'abi': abi})
        else:
            raise ValueError('ABI json file not loaded')
