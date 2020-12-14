from base64 import b64encode, decodebytes
from binascii import Error
from notarizer.exceptions import InvalidLabelSignature


def bytes_to_str(content: bytes, encoding="utf-8") -> str:
    return str(content, encoding=encoding)


def encode_to_base64(content: bytes) -> bytes:
    try:
        result = b64encode(content)
        return result
    except Error as err:
        raise InvalidLabelSignature(str(err))


def decode_from_base64(content: str, encoding="utf-8") -> bytes:
    try:
        result = decodebytes(str_to_bytes(content, encoding))
        return result
    except Error as err:
        raise InvalidLabelSignature(str(err))


def str_to_bytes(content: str, encoding="utf-8") -> bytes:
    return bytes(content, encoding)
