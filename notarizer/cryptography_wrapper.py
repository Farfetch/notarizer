from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature

from notarizer.converter import str_to_bytes, bytes_to_str, encode_to_base64
from notarizer.exceptions import VerificationFailure


def verify(public_key: bytes, signature: bytes, content: str):
    try:
        public_key_pem = load_pem_public_key(public_key, default_backend())
        public_key_pem.verify(
            signature,
            str_to_bytes(content),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
    except InvalidSignature:
        raise VerificationFailure("Invalid Signature")


def create_signature(private_key: bytes, content: str) -> str:
    private_key_pem = load_pem_private_key(private_key, password=None, backend=default_backend())

    signature = private_key_pem.sign(
        str_to_bytes(content),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )

    encoded_signature = encode_to_base64(signature)
    signature_text = bytes_to_str(encoded_signature)

    return signature_text
