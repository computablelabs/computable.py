from computable.contracts.deployed import Deployed


class Datatrust(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'datatrust.abi')
