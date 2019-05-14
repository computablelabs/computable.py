from web3 import Web3

# why does web3.py use camelCase?
GAS_PRICE = Web3.toWei(2, 'gwei')
# min amount of gas for any operation, used for call types as we don't pull that gas from the ABI
MIN_GAS = 21000
# web3 will buffer estimated gas amounts by 100k so we'll do the same
GAS_BUFFER = 100000

SECONDS_IN_A_DAY = 86400

# parameterizer attributes are integers
STAKE = 1
PRICE_FLOOR = 2
SPREAD = 4
LIST_REWARD = 5
PLURALITY = 6
VOTE_BY = 7
BACKEND_PAYMENT = 8
MAKER_PAYMENT = 9
COST_PER_BYTE = 11

# sole candidate 'kind' know to the parameterizer
REPARAM = 3
