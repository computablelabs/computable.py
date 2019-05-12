from computable.contracts.deployed import Deployed

class Voting(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'voting.abi')

    def candidate_is(self, hash, kind, opts=None):
        """
        @param hash The keccak256 identifier for this candidate
        @param opts Optional callOpts for this view/constant type call
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('candidateIs')}, opts)
        return self.deployed.functions.candidateIs(hash, kind).call(opts)

    def is_candidate(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('isCandidate')}, opts)
        return self.deployed.functions.isCandidate(hash).call(opts)

    def get_candidate(self, hash, opts=None):
        """
        @return (kind, owner, stake, vote_by, yea, nay)
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getCandidate')}, opts)
        return self.deployed.functions.getCandidate(hash).call(opts)

    def get_candidate_owner(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getCandidateOwner')}, opts)
        return self.deployed.functions.getCandidateOwner(hash).call(opts)

    def did_pass(self, hash, plurality, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('didPass')}, opts)
        return self.deployed.functions.didPass(hash, plurality).call(opts)

    def poll_closed(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('pollClosed')}, opts)
        return self.deployed.functions.pollClosed(hash).call(opts)

    def vote(self, hash, option, opts=None):
        """
        @param option Either the integer `1` for a "yea" vote or any other value
        which is translated as a "nay"
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('vote')}, opts)
        return self.deployed.functions.vote(hash, option).transact(opts)

    def get_stake(self, hash, addr, opts=None):
        """
        @param addr Address that a possible staked amount, in Market Token, belongs to
        @return Staked amount in wei
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getStake')}, opts)
        return self.deployed.functions.getStake(hash, addr).call(opts)

    def unstake(self, hash, opts=None):
        """
        Claim any staked amounts that an address has rights to
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('unstake')}, opts)
        return self.deployed.functions.unstake(hash).transact(opts)
