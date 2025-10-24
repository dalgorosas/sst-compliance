from __future__ import annotations

import json
import logging
from functools import cached_property
from typing import Any

try:  # pragma: no cover - import opcional
    import gspread
except ModuleNotFoundError:  # pragma: no cover - dependencia opcional
    gspread = None  # type: ignore[assignment]

try:  # pragma: no cover - import opcional
    from google.oauth2.service_account import Credentials
except ModuleNotFoundError:  # pragma: no cover - dependencia opcional
    Credentials = None  # type: ignore[assignment]

from app.core.config import settings

logger = logging.getLogger(__name__)


class GoogleSheetsRegistry:
    """Cliente auxiliar para registrar usuarios en Google Sheets."""

    SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)

    def __init__(
        self,
        spreadsheet_id: str | None = None,
        worksheet_name: str | None = None,
    ) -> None:
        self._spreadsheet_id = spreadsheet_id or settings.GOOGLE_SHEETS_USER_SPREADSHEET_ID
        self._worksheet_name = worksheet_name or settings.GOOGLE_SHEETS_USER_WORKSHEET

    @cached_property
    def _credentials(self) -> Credentials | None:
        """Construye las credenciales del servicio, si la configuración está presente."""

        if not Credentials:
            logger.error("No está instalado google-auth; se omite Google Sheets")
            return None

        if settings.GOOGLE_SERVICE_ACCOUNT_JSON:
            try:
                data: dict[str, Any] = json.loads(settings.GOOGLE_SERVICE_ACCOUNT_JSON)
            except json.JSONDecodeError as exc:  # pragma: no cover - dependencia externa
                logger.error("Configuración JSON de Google inválida: %s", exc)
                return None
            return Credentials.from_service_account_info(data, scopes=self.SCOPES)

        if settings.GOOGLE_SERVICE_ACCOUNT_FILE:
            try:
                return Credentials.from_service_account_file(
                    settings.GOOGLE_SERVICE_ACCOUNT_FILE,
                    scopes=self.SCOPES,
                )
            except OSError as exc:  # pragma: no cover - dependiente de entorno
                logger.error("No se pudo leer el archivo de credenciales de Google: %s", exc)
                return None

        return None

    @cached_property
    def _worksheet(self):  # pragma: no cover - interacción externa
        if not gspread:
            raise RuntimeError("No está instalado gspread")

        creds = self._credentials
        if not creds:
            raise RuntimeError("Credenciales de Google Sheets no configuradas correctamente")
        if not self._spreadsheet_id or not self._worksheet_name:
            raise RuntimeError("Falta configurar el ID de la hoja y la pestaña de Google Sheets")

        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(self._spreadsheet_id)
        return spreadsheet.worksheet(self._worksheet_name)

    @property
    def is_configured(self) -> bool:
        """Indica si existen los parámetros mínimos para operar."""

        return bool(
            (self._spreadsheet_id and self._worksheet_name)
            and (settings.GOOGLE_SERVICE_ACCOUNT_JSON or settings.GOOGLE_SERVICE_ACCOUNT_FILE)
            and Credentials
            and gspread
        )

    def register_user(self, *, email: str, hashed_password: str, role: str) -> None:
        """Agrega una fila con la información básica del usuario."""

        if not self.is_configured:
            logger.info(
                "Registro en Google Sheets omitido: configuración incompleta"
            )
            return

        try:
            worksheet = self._worksheet
            worksheet.append_row(
                [email, hashed_password, role],
                value_input_option="USER_ENTERED",
            )
        except Exception as exc:  # pragma: no cover - dependiente del API externo
            logger.error("No se pudo registrar el usuario en Google Sheets: %s", exc)
            