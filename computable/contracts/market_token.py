from computable.contracts.erc20 import ERC20

class MarketToken(ERC20):
    def at(self, w3, address):
        super().at(w3, address, 'markettoken.abi')
