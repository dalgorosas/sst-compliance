from __future__ import annotations

import logging
from typing import Iterable

logger = logging.getLogger(__name__)


class AlertService:
    def send_email(self, to: str, subject: str, body: str) -> None:
        logger.info("Enviando correo a %s con asunto %s", to, subject)
        logger.debug("Contenido: %s", body)

    def broadcast(self, recipients: Iterable[str], message: str) -> None:
        for recipient in recipients:
            self.send_email(recipient, "Notificación SST", message)