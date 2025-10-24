from __future__ import annotations

import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_REGEX = re.compile(r"^[0-9+\- ]{6,20}$")
RUC_REGEX = re.compile(r"^[0-9]{9,13}$")


def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))


def validate_ruc(ruc: str) -> bool:
    return bool(RUC_REGEX.match(ruc))