from __future__ import annotations

import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta
from typing import Any, TypedDict

from app.core.config import settings


class TokenData(TypedDict):
    sub: str
    exp: int


class PasswordManager:
    """Herramientas de hashing y verificación de contraseñas."""

    algorithm = "sha256"
    iterations = 260000

    @staticmethod
    def hash_password(password: str, salt: bytes | None = None) -> str:
        if salt is None:
            salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac(
            PasswordManager.algorithm, password.encode("utf-8"), salt, PasswordManager.iterations
        )
        return base64.b64encode(salt + dk).decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        decoded = base64.b64decode(hashed.encode("utf-8"))
        salt, stored = decoded[:16], decoded[16:]
        new_hash = hashlib.pbkdf2_hmac(
            PasswordManager.algorithm, password.encode("utf-8"), salt, PasswordManager.iterations
        )
        return hmac.compare_digest(stored, new_hash)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = f"{subject}|{int(expire.timestamp())}"
    signature = hmac.new(settings.SECRET_KEY.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256).digest()
    token = base64.urlsafe_b64encode(payload.encode("utf-8") + b"." + signature).decode("utf-8")
    return token


def decode_access_token(token: str) -> TokenData:
    raw = base64.urlsafe_b64decode(token.encode("utf-8"))
    payload_part, signature_part = raw.split(b".")
    expected_signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"), payload_part, hashlib.sha256
    ).digest()
    if not hmac.compare_digest(signature_part, expected_signature):
        raise ValueError("Token inválido")
    subject, exp_str = payload_part.decode("utf-8").split("|")
    exp = int(exp_str)
    if datetime.utcnow().timestamp() > exp:
        raise ValueError("Token expirado")
    return TokenData(sub=subject, exp=exp)
