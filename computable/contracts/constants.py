from web3 import Web3

# why does web3.py use camelCase?
GAS_PRICE = Web3.toWei(2, 'gwei')
# bit of rando here, as GAS should likely always be passed by user
GAS = 150000
