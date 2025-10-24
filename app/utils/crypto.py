from __future__ import annotations

import hashlib
from secrets import token_urlsafe


def hash_sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def generate_token(length: int = 32) -> str:
    return token_urlsafe(length)


def generate_file_hash(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()