import json
from computable.contracts.deployed import Deployed


class Datatrust(Deployed):
    def at(self, w3, address):
        abi = None
        path = os.path.join(os.path.dirname(__file__), 'datatrust.abi')
        with open(path) as f:
            abi = json.loads(f.read())
        if abi is not None:
            super().at(w3, {'address': address, 'abi': abi})
        else:
            raise ValueError('ABI json file not loaded')
