from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


def now_utc() -> datetime:
    return datetime.now(tz=ZoneInfo("UTC"))


def to_timezone(value: datetime, timezone: str) -> datetime:
    if value.tzinfo is None:
        value = value.replace(tzinfo=ZoneInfo("UTC"))
    return value.astimezone(ZoneInfo(timezone))