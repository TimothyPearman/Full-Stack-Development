from typing import Set
import threading    # used to prevent tokens from being modified by multiple endpoints at once

class TokenDenylist:
    """storage for revoked tokens"""
    
    def __init__(self):
        self._denylisted_tokens: Set[str] = set()           # store revoked tokens in a set
        self._lock = threading.Lock()                       # lock to ensure thread safety when modifying the denylist
    
    def add(self, token: str):
        """add a token to the denylist"""
        with self._lock:                                    # lock the denylist while modifying
            self._denylisted_tokens.add(token)              # add the token to set
        
        return None
    
    def check(self, token: str):
        """check if a token is denylisted"""
        with self._lock:                                    # lock the denylist while checking
            return token in self._denylisted_tokens         # return if the token is in the set of revoked tokens

_denylist = TokenDenylist()                                 # create a global denylist instance

def revoke_token(token: str):
    """revoke a token"""
    _denylist.add(token)

    return None


def is_token_revoked(token: str):
    """check if a token has been revoked"""

    return _denylist.check(token)
