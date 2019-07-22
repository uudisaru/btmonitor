from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def is_encrypted_rsa_key(private_key: str) -> bool:
    return 'RSA' in private_key and 'ENCRYPTED' in private_key


def decrypt_private_key(private_key: str, enc_pwd: str):
    return serialization.load_pem_private_key(
        bytes(private_key, 'utf-8'),
        password=bytes(enc_pwd, 'utf-8'),
        backend=default_backend(),
    )
