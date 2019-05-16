from computable.contracts.deployed import Deployed

class Datatrust(Deployed):
    def at(self, w3, address):
        super().at(w3, address, 'datatrust.abi')

    def set_privileged(self, listing, opts=None):
        """
        @param listing Address
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setPrivileged')}, opts)
        return self.deployed.functions.setPrivileged(listing).transact(opts)

    def get_privileged(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getPrivileged')}, opts)
        return self.deployed.functions.getPrivileged().call(opts)

    def get_hash(self, url, opts=None):
        """
        @param url String (max 128 chars) which is the url of a datatrust
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getHash')}, opts)
        return self.deployed.functions.getHash(url).call(opts)

    def get_backend_address(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBackendAddress')}, opts)
        return self.deployed.functions.getBackendAddress().call(opts)

    def get_backend_url(self, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBackendUrl')}, opts)
        return self.deployed.functions.getBackendUrl().call(opts)

    def set_backend_url(self, url, opts=None):
        """
        Allow an already registered datatrust to change its URL
        @param url String (max 128 chars) which is the url of a datatrust
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setBackendUrl')}, opts)
        return self.deployed.functions.setBackendUrl(url).transact(opts)

    def set_data_hash(self, listing, data, opts=None):
        """
        @param listing A listing hash (keccak256) identifier
        @param data A keccack256 hash of the actual data for said listing
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('setDataHash')}, opts)
        return self.deployed.functions.setDataHash(listing, data).transact(opts)

    def register(self, url, opts=None):
        """
        @param url String (max 128 chars) which is the url of a datatrust
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('register')}, opts)
        return self.deployed.functions.register(url).transact(opts)

    def resolve_registration(self, hash, opts=None):
        """
        @param hash Keccack256 hash of the registration candidate's URL
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('resolveRegistration')}, opts)
        return self.deployed.functions.resolveRegistration(hash).transact(opts)

    def request_delivery(self, hash, amount, opts=None):
        """
        @param hash Keccack256 hash of a delivery-query recieved from a demand buyer
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('requestDelivery')}, opts)
        return self.deployed.functions.requestDelivery(hash, amount).transact(opts)

    def get_bytes_purchased(self, addr, opts=None):
        opts = self.assign_transact_opts({'gas': self.get_gas('getBytesPurchased')}, opts)
        return self.deployed.functions.getBytesPurchased(addr).call(opts)

    def get_delivery(self, hash, opts=None):
        """
        @return (owner, bytes_requested, bytes_delivered)
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getDelivery')}, opts)
        return self.deployed.functions.getDelivery(hash).call(opts)

    def listing_accessed(self, listing, delivery, amount, opts=None):
        """
        @param listing Keccack256 Listing hash identifier
        @param delivery keccack256 Delivery object identifier
        @param amount Number of bytes accessed from said listing
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('listingAccessed')}, opts)
        return self.deployed.functions.listingAccessed(listing, delivery, amount).transact(opts)

    def get_bytes_accessed(self, hash, opts=None):
        """
        Returns the total unclaimed amount of byte access a Listing has accumulated
        @param hash Keccack256 hash Listing identifier
        """
        opts = self.assign_transact_opts({'gas': self.get_gas('getBytesAccessed')}, opts)
        return self.deployed.functions.getBytesAccessed(hash).call(opts)

    def delivered(self, delivery, url, opts=None):
        """
        @param delivery Keccack256 hash identifier of the Delivery object
        @param url Keccack256 hash of some location that the datatrust delivered to
        """
        # TODO we could check length of the url here and raise...
        opts = self.assign_transact_opts({'gas': self.get_gas('delivered')}, opts)
        return self.deployed.functions.delivered(delivery, url).transact(opts)
