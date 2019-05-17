from computable.contracts.deployed import Deployed

class Listing(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'listing.abi')

    def is_listed(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('isListed')}, opts)
        return self.deployed.functions.isListed(hash).call(opts)

    def withdraw_from_listing(self, hash, amount, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('withdrawFromListing')}, opts)
        return self.deployed.functions.withdrawFromListing(hash, amount).transact(opts)

    def list(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('list')}, opts)
        return self.deployed.functions.list(hash).transact(opts)

    def get_listing(self, hash, opts=None):
        """
        @return (owner, supply)
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getListing')}, opts)
        return self.deployed.functions.getListing(hash).call(opts)

    def resolve_application(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('resolveApplication')}, opts)
        return self.deployed.functions.resolveApplication(hash).transact(opts)

    def claim_bytes_accessed(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('claimBytesAccessed')}, opts)
        return self.deployed.functions.claimBytesAccessed(hash).transact(opts)

    def challenge(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('challenge')}, opts)
        return self.deployed.functions.challenge(hash).transact(opts)

    def resolve_challenge(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('resolveChallenge')}, opts)
        return self.deployed.functions.resolveChallenge(hash).transact(opts)

    def exit(self, hash, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('exit')}, opts)
        return self.deployed.functions.exit(hash).transact(opts)
