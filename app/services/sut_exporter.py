from __future__ import annotations

from typing import Any, Iterable

from app.models.cumplimiento import Cumplimiento
from app.models.incidente import Incidente


class SUTExporter:
    """Genera estructuras de datos exportables al Sistema Único de Trabajo (SUT)."""

    def export(self, cumplimientos: Iterable[Cumplimiento], incidentes: Iterable[Incidente]) -> dict[str, Any]:
        return {
            "cumplimientos": [
                {
                    "normativa": c.normativa,
                    "requisito": c.requisito,
                    "estado": c.estado.value,
                    "evidencia": c.evidencia,
                }
                for c in cumplimientos
            ],
            "incidentes": [
                {
                    "titulo": i.titulo,
                    "severidad": i.severidad.value,
                    "fecha": i.fecha.isoformat(),
                }
                for i in incidentes
            ],
        }