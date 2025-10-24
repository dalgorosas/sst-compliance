from __future__ import annotations

import logging
from logging.config import dictConfig


def configure_logging(level: int | str = logging.INFO) -> None:
    """Configura un logger uniforme para toda la aplicación."""

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": level,
            }
        },
        "root": {
            "handlers": ["console"],
            "level": level,
        },
    }
    dictConfig(logging_config)
    