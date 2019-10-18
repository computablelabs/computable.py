from computable.contracts.deployed import Deployed

class Datatrust(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'datatrust')

    def set_privileged(self, listing, opts=None):
        """
        @param listing Address
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setPrivileged')}, opts)
        return self.deployed.functions.setPrivileged(listing), opts

    def get_privileged(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getPrivileged')}, opts)
        return self.deployed.functions.getPrivileged(), opts

    def get_reserve(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getReserve')}, opts)
        return self.deployed.functions.getReserve(), opts

    def get_hash(self, url, opts=None):
        """
        @param url String (max 128 chars) which is the url of a datatrust
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getHash')}, opts)
        return self.deployed.functions.getHash(url), opts

    def get_backend_address(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBackendAddress')}, opts)
        return self.deployed.functions.getBackendAddress(), opts

    def get_backend_url(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBackendUrl')}, opts)
        return self.deployed.functions.getBackendUrl(), opts

    def set_backend_url(self, url, opts=None):
        """
        Allow an already registered datatrust to change its URL
        @param url String (max 128 chars) which is the url of a datatrust
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setBackendUrl')}, opts)
        return self.deployed.functions.setBackendUrl(url), opts

    def get_data_hash(self, listing, opts=None):
        """
        @param listing A listing hash (keccak256) identifier
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getDataHash')}, opts)
        return self.deployed.functions.getDataHash(listing), opts

    def set_data_hash(self, listing, data, opts=None):
        """
        @param listing A listing hash (keccak256) identifier
        @param data A keccack256 hash of the actual data for said listing
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setDataHash')}, opts)
        return self.deployed.functions.setDataHash(listing, data), opts

    def register(self, url, opts=None):
        """
        @param url String (max 128 chars) which is the url of a datatrust
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('register')}, opts)
        return self.deployed.functions.register(url), opts

    def resolve_registration(self, hash, opts=None):
        """
        @param hash Keccack256 hash of the registration candidate's URL
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('resolveRegistration')}, opts)
        return self.deployed.functions.resolveRegistration(hash), opts

    def request_delivery(self, hash, amount, opts=None):
        """
        @param hash Keccack256 hash of a delivery-query recieved from a demand buyer
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('requestDelivery')}, opts)
        return self.deployed.functions.requestDelivery(hash, amount), opts

    def get_bytes_purchased(self, addr, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBytesPurchased')}, opts)
        return self.deployed.functions.getBytesPurchased(addr), opts

    def get_delivery(self, hash, opts=None):
        """
        @return (owner, bytes_requested, bytes_delivered)
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getDelivery')}, opts)
        return self.deployed.functions.getDelivery(hash), opts

    def listing_accessed(self, listing, delivery, amount, opts=None):
        """
        @param listing Keccack256 Listing hash identifier
        @param delivery keccack256 Delivery object identifier
        @param amount Number of bytes accessed from said listing
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('listingAccessed')}, opts)
        return self.deployed.functions.listingAccessed(listing, delivery, amount), opts

    def get_access_reward_earned(self, hash, opts=None):
        """
        Returns the total unclaimed amount of access reward a Listing has accumulated
        @param hash Keccack256 hash Listing identifier
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getAccessRewardEarned')}, opts)
        return self.deployed.functions.getAccessRewardEarned(hash), opts

    def delivered(self, delivery, url, opts=None):
        """
        @param delivery Keccack256 hash identifier of the Delivery object
        @param url Keccack256 hash of some location that the datatrust delivered to
        """
        # TODO we could check length of the url here and raise...
        opts = self.assign_transact_opts({'gas': self.get_gas('delivered')}, opts)
        return self.deployed.functions.delivered(delivery, url), opts
