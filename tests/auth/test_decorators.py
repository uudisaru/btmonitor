from . import read_key
from btmonitor.auth.decorators import authorized
from btmonitor.auth.decorators import cleanup
from btmonitor.auth.jwt_auth import create_token
from sanic.config import Config
from sanic.response import json
from unittest.mock import Mock

import pytest


@pytest.fixture()
def token():
    return create_token({}, read_key('test.key'))


@pytest.fixture()
def public_key():
    return read_key('test.pub')


def make_auth_func(public_key, alg=None):
    config = Config()
    config.PUBLIC_KEY = public_key
    if alg:
        config.ALGORITHM = alg

    @authorized(config)
    async def f(request):
        return json({'status': 'OK'}, 200)

    return f


@pytest.fixture(params=[None, 'RS256'])
def auth_func(public_key, request):
    config = Config()
    config.PUBLIC_KEY = public_key
    if request.param:
        config.ALGORITHM = request.param

    @authorized(config)
    async def f(request):
        return json({'status': 'OK'}, 200)

    return f


def test_cleanup(public_key):
    key = public_key.replace('\n', ' ')
    assert public_key == cleanup(key)


def test_cleanup_invalid():
    invalid = 'non-PEM encoded text'
    assert invalid == cleanup(invalid)


@pytest.mark.asyncio
async def test_auth_success(token, auth_func):
    req = Mock()
    req.headers = Mock()
    req.headers.get = Mock(return_value='Bearer ' + str(token, 'utf-8'))
    res = await auth_func(req)
    assert res.status == 200


@pytest.mark.asyncio
async def test_auth_no_token(auth_func):
    req = Mock()
    req.headers = Mock()
    req.headers.get = Mock(return_value=None)
    res = await auth_func(req)
    assert res.status == 403
    req.headers.get = Mock(return_value='invalid')
    res = await auth_func(req)
    assert res.status == 403


@pytest.mark.asyncio
async def test_auth_invalid_token(auth_func):
    req = Mock()
    req.headers = Mock()
    req.headers.get = Mock(return_value='Bearer invalid')
    res = await auth_func(req)
    assert res.status == 403
