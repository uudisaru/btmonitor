from btmonitor.auth.jwt_auth import validate_token
from functools import lru_cache
from functools import wraps
from jwt import PyJWTError
from sanic.config import Config
from sanic.request import Request
from sanic.response import json

import logging
import re


logger = logging.getLogger(__name__)
PEM_REGEX = re.compile(
    r"^(-+BEGIN .*KEY-+)(.*?)(-+END .*KEY-+)\s*$", re.DOTALL | re.X
)


@lru_cache(maxsize=32)
def cleanup(pem):
    """Restore newlines of PEM-encoded key file"""
    m = PEM_REGEX.match(pem)
    if m:
        return m.group(1) + m.group(2).replace(' ', '\n') + m.group(3) + '\n'
    return pem


def validate_auth(request: Request, config: Config) -> bool:
    bearer_token = request.headers.get('Authorization', '')
    if bearer_token and bearer_token.startswith('Bearer '):
        index = len('Bearer ')
        token = bearer_token[index:].strip()
        params = {}
        if 'PUBLIC_KEY' in config:
            params['public_key'] = cleanup(config.PUBLIC_KEY)
        if 'ALGORITHM' in config:
            params['algorithm'] = config.ALGORITHM
        try:
            validate_token(bytes(token, encoding='utf-8'), **params)
            return True
        except PyJWTError as exc:
            logger.error('Unauthorized access (ip %s): %s', request.ip, exc)
    return False


def authorized(config: Config):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            if validate_auth(request, config):
                return await f(request, *args, **kwargs)
            else:
                return json({'status': 'not_authorized'}, 403)

        return decorated_function

    return decorator
