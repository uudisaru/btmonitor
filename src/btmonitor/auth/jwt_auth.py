from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from math import floor
from typing import Dict
from typing import Union

import jwt
import time


def create_token(
    payload: Dict[str, Union[str, int]],
    private_key: Union[str, RSAPrivateKey],
    algorithm: str = 'RS256',
) -> bytes:
    """
    Create JSON Web Token (validity 15 minutes).
    :raises InvalidKeyError if provided key is in incorrect format
    """
    iat = floor(time.time())
    claims = dict(payload)
    claims['iat'] = iat
    claims['exp'] = iat + 15 * 60
    claims['iss'] = 'btmonitor'
    return jwt.encode(claims, private_key, algorithm=algorithm)


def validate_token(
    token: bytes, public_key: str, algorithm: str = 'RS256'
) -> Dict[str, Union[str, int]]:
    """
    Read and validate JSON Web Token.
    :raises InvalidTokenError if decoding fails (expired token,
                                                 invalid signature etc)
    :raises InvalidKeyError if provided key is in incorrect format
    """
    return jwt.decode(token, public_key, algorithms=[algorithm])
