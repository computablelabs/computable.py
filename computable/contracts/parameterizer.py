from computable.contracts.deployed import Deployed

class Parameterizer(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'parameterizer.abi')

    def get_backend_payment(self, opts=None):
        return self.deployed.functions.getBackendPayment().call(opts)

    def get_maker_payment(self, opts=None):
        return self.deployed.functions.getMakerPayment().call(opts)

    def get_reserve_payment(self, opts=None):
        return self.deployed.functions.getReservePayment().call(opts)

    def get_cost_per_byte(self, opts=None):
        return self.deployed.functions.getCostPerByte().call(opts)

    def get_stake(self, opts=None):
        return self.deployed.functions.getStake().call(opts)

    def get_price_floor(self, opts=None):
        return self.deployed.functions.getPriceFloor().call(opts)

    def get_hash(self, param, value, opts=None):
        """
        @param param Integer representing one of the parameterizer attributes
        @param value Integer for the value of said attribute
        @return a Keccak256 hash of the values
        NOTE: You can likely use web3's `soliditySha3(['uint256', 'uint256'], [p, v])` as well
        """
        return self.deployed.functions.getHash(param, value).call(opts)

    def get_spread(self, opts=None):
        return self.deployed.functions.getSpread().call(opts)

    def get_list_reward(self, opts=None):
        return self.deployed.functions.getListReward().call(opts)

    def get_plurality(self, opts=None):
        return self.deployed.functions.getPlurality().call(opts)

    def get_reparam(self, hash, opts=None):
        """
        @param hash Keccak256 hash that is a Reparam identifier
        @return (param, value)
        """
        return self.deployed.functions.getReparam(hash).call(opts)

    def get_vote_by(self, opts=None):
        return self.deployed.functions.getVoteBy().call(opts)

    def reparameterize(self, param, value, opts):
        opts = self.assign_transact_opts({}, opts)
        return self.deployed.functions.reparameterize(param, value).transact(opts)
