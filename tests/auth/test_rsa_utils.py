from . import read_key
from btmonitor.auth.rsa_utils import decrypt_private_key
from btmonitor.auth.rsa_utils import is_encrypted_rsa_key
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

import pytest


@pytest.fixture()
def private_key():
    return read_key('test.key')


@pytest.fixture()
def enc_private_key():
    return read_key('test.enc.key')


def test_is_encrypted_rsa_key(enc_private_key, private_key):
    assert is_encrypted_rsa_key(enc_private_key)
    assert not is_encrypted_rsa_key(private_key)


def test_decrypt_private_key(enc_private_key):
    assert isinstance(
        decrypt_private_key(enc_private_key, '1234'), RSAPrivateKey
    )
