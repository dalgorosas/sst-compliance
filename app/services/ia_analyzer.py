from __future__ import annotations

from statistics import mean
from typing import Iterable

from app.models.cumplimiento import Cumplimiento, EstadoCumplimiento
from app.models.incidente import Incidente, SeveridadIncidente


class IAAnalyzer:
    """Heurística simple que simula un análisis asistido por IA."""

    def risk_score(self, cumplimientos: Iterable[Cumplimiento], incidentes: Iterable[Incidente]) -> float:
        cumplimientos_list = list(cumplimientos)
        incidentes_list = list(incidentes)
        cumplimiento_ratio = 0.0
        if cumplimientos_list:
            cumplidos = sum(1 for c in cumplimientos_list if c.estado == EstadoCumplimiento.CUMPLIDO)
            cumplimiento_ratio = cumplidos / len(cumplimientos_list)
        severidades = [self._severity_weight(i.severidad) for i in incidentes_list] or [0]
        incidente_promedio = mean(severidades)
        score = max(0.0, 100 * cumplimiento_ratio - incidente_promedio * 20)
        return round(score, 2)

    def recommendations(self, cumplimientos: Iterable[Cumplimiento], incidentes: Iterable[Incidente]) -> list[str]:
        recomendaciones: list[str] = []
        for c in cumplimientos:
            if c.estado != EstadoCumplimiento.CUMPLIDO:
                recomendaciones.append(f"Completar requisito {c.requisito} de la normativa {c.normativa}.")
        for incidente in incidentes:
            if incidente.severidad in {SeveridadIncidente.ALTA, SeveridadIncidente.CRITICA}:
                recomendaciones.append(f"Revisar plan de acción del incidente '{incidente.titulo}'.")
        return recomendaciones

    def _severity_weight(self, severidad: SeveridadIncidente) -> int:
        mapping = {
            SeveridadIncidente.BAJA: 1,
            SeveridadIncidente.MEDIA: 2,
            SeveridadIncidente.ALTA: 3,
            SeveridadIncidente.CRITICA: 5,
        }
        return mapping[severidad]