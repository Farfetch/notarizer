from notarizer.exceptions import PrivateKeyNotFound, PublicKeyNotFound


def load_public_key(file_path: str) -> bytes:
    try:
        return _read_file(file_path)
    except OSError:
        raise PublicKeyNotFound()


def load_private_key(file_path: str) -> bytes:
    try:
        return _read_file(file_path)
    except OSError:
        raise PrivateKeyNotFound()


def _read_file(path: str) -> bytes:
    with open(path, "rb") as key_file:
        key_bytes = key_file.read().strip()
        return key_bytes
