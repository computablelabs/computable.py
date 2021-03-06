from computable.contracts.deployed import Deployed

class Parameterizer(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'parameterizer')

    def get_backend_payment(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBackendPayment')}, opts)
        return self.deployed.functions.getBackendPayment(), opts

    def get_maker_payment(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getMakerPayment')}, opts)
        return self.deployed.functions.getMakerPayment(), opts

    def get_reserve_payment(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getReservePayment')}, opts)
        return self.deployed.functions.getReservePayment(), opts

    def get_cost_per_byte(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getCostPerByte')}, opts)
        return self.deployed.functions.getCostPerByte(), opts

    def get_stake(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getStake')}, opts)
        return self.deployed.functions.getStake(), opts

    def get_price_floor(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getPriceFloor')}, opts)
        return self.deployed.functions.getPriceFloor(), opts

    def get_hash(self, param, value, opts=None):
        """
        @param param Integer representing one of the parameterizer attributes
        @param value Integer for the value of said attribute
        @return a Keccak256 hash of the values
        NOTE: You can likely use web3's `soliditySha3(['uint256', 'uint256'], [p, v])` as well
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getHash')}, opts)
        return self.deployed.functions.getHash(param, value), opts

    def get_spread(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getSpread')}, opts)
        return self.deployed.functions.getSpread(), opts

    def get_list_reward(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getListReward')}, opts)
        return self.deployed.functions.getListReward(), opts

    def get_plurality(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getPlurality')}, opts)
        return self.deployed.functions.getPlurality(), opts

    def get_reparam(self, hash, opts=None):
        """
        @param hash Keccak256 hash that is a Reparam identifier
        @return (param, value)
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getReparam')}, opts)
        return self.deployed.functions.getReparam(hash), opts

    def get_vote_by(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getVoteBy')}, opts)
        return self.deployed.functions.getVoteBy(), opts

    def reparameterize(self, param, value, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('reparameterize')}, opts)
        return self.deployed.functions.reparameterize(param, value), opts

    def resolve_reparam(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('resolveReparam')}, opts)
        return self.deployed.functions.resolveReparam(hash), opts
