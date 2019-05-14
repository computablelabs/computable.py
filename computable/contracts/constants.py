from web3 import Web3

# why does web3.py use camelCase?
GAS_PRICE = Web3.toWei(2, 'gwei')
# min amount of gas for any operation, used for call types as we don't pull that gas from the ABI
MIN_GAS = 21000
# web3 will buffer estimated gas amounts by 100k so we'll do the same
GAS_BUFFER = 100000

SECONDS_IN_A_DAY = 86400
