from datetime import datetime, timedelta, timezone
import os
from uuid import uuid4

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.token import is_token_revoked


DEFAULT_SECRET_KEY = "secret-key-making-this-longer-becuase-it-needs-to-be-32-bytes-:D"     # default secret key for development

SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)                                    # secret key used for signing JWT tokens
ALGORITHM = "HS256"                                                                         # algorithm used for signing JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))            # token lifetime

def create_access_token(user_id: int):
    """Create a JWT access token for a given user id"""
    expire_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # set the expiration time for the token
    payload = {                                                                             # what the token contains
        "sub": str(user_id),                                                                # subject of the token
        "exp": expire_at,                                                                   # expiration time of the token
        "iat": datetime.now(timezone.utc),                                                  # issued-at time to avoid identical tokens in quick succession
        "jti": str(uuid4()),                                                                # unique token id for denylist isolation
    }
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_user_id_from_token(token: str) -> int:
    """decode a JWT token"""
    try:
        if is_token_revoked(token):                                                         # check if the token has been revoked
            raise InvalidTokenError("Token has been revoked")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])                     # decode the token and verify its signature and expiration
        subject = payload.get("sub")                                                        # get the subject claim from the token (user_id)   

        if subject is None:                                                                 # check if the subject claim is present in the token
            raise InvalidTokenError("Missing token subject")        
        
        return int(subject)
    
    except ExpiredSignatureError:                                                           # check if the token has expired
        raise InvalidTokenError("Token has expired")
    
    except (InvalidTokenError, ValueError, TypeError):                                      # check if the token is invalid
        raise InvalidTokenError("Invalid token")