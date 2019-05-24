#  NOTE: Send type transactions have their operations isolated for maximum flexability

#  base_tx, opts = token.approve(addr, amt, opts)
#  built_tx = build_transaction(w3, base_tx, opts)
#  signed_tx = sign_transaction(w3, built_tx, private_key)
#  final_tx = send_raw_transaction(w3, signed_tx)

#  The `send` method abstracts this into a single call, similar to `call` for convenience
#  tx = send(w3, private_key, token.approve(addr, amt))

def call(args):
    """
    Call type operations do not need be signed

    ex:
    spam = call(token.allowance(addr, addr))

    @param args A tuple which is always [tx, opts]
    """
    return args[0].call(args[1])

def transact(args):
    """
    If working with unlocked accounts we can simply use the transact method
    See `call`
    """
    return args[0].transact(args[1])

def build_transaction(w3, args):
    """
    Return a suitable transaction object for signing.
    NOTE: We assume the opts object has been prehydrated with a HOC's `assign_transact_opts`
    """
    args[1]['nonce'] = w3.eth.getTransactionCount(args[1]['from'])
    return args[0].buildTransaction(args[1])

def sign_transaction(w3, private_key, tx):
    """
    Called after a transaction has been built, perhaps with `build_transaction`
    """
    return w3.eth.account.signTransaction(tx, private_key=private_key)

def send_raw_transaction(w3, tx):
    """
    Given a signed transaction, broadcast it.
    """
    return w3.eth.sendRawTransaction(tx.rawTransaction)

def send(w3, private_key, args):
    """
    Convenience method to take a built transaction, sign it and broadcast it using existing methods
    """
    built_tx = build_transaction(w3, args)
    signed_tx = sign_transaction(w3, private_key, built_tx)
    return send_raw_transaction(w3, signed_tx)
