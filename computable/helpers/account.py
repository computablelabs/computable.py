from computable.helpers.constants import UNLOCK_DURATION

def unlock(w3, phrase, acct=None, timeout=None):
    """
    @param w3 The current instantiation of Web3
    @param acct An account to unlock. Defaults to the w3 default acct
    @param timeout How long to unlock the account for. Defaults to constant
    """
    if acct is None:
        acct = w3.eth.defaultAccount
    if timeout is None:
        timeout = UNLOCK_DURATION
    return w3.personal.unlockAccount(acct, phrase, timeout)

def lock(w3, acct=None):
    if acct is None:
        acct = w3.eth.defaultAccount
    return w3.personal.lockAccount(acct)
