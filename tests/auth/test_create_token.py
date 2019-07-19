from . import read_key
from btmonitor.auth.jwt_auth import create_token
from btmonitor.auth.jwt_auth import validate_token

import pytest


@pytest.fixture()
def private_key():
    return read_key('test.key')


@pytest.fixture()
def public_key():
    return read_key('test.pub')


def test_create_token(private_key):
    token = create_token({}, private_key, 'RS256')
    assert token is not None


def test_validate_token(private_key, public_key):
    token = create_token({}, private_key, 'RS256')
    assert validate_token(token, public_key)
