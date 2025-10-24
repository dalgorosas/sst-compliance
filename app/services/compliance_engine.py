from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from app.models.cumplimiento import Cumplimiento, EstadoCumplimiento
from app.models.incidente import Incidente, SeveridadIncidente


class ComplianceEngine:
    """Lógica de negocio para evaluar el cumplimiento de una empresa."""

    def evaluate_company(
        self,
        cumplimientos: Iterable[Cumplimiento],
        incidentes: Iterable[Incidente],
    ) -> dict[str, Any]:
        cumplimiento_counter = Counter(c.estado for c in cumplimientos)
        incidentes_counter = Counter(i.severidad for i in incidentes)
        score = self._score(cumplimiento_counter, incidentes_counter)
        return {
            "score": score,
            "cumplimientos": dict(cumplimiento_counter),
            "incidentes": dict(incidentes_counter),
            "riesgo": self._risk_level(score, incidentes_counter),
        }

    def _score(self, cumplimiento_counter: Counter, incidentes_counter: Counter) -> float:
        total = sum(cumplimiento_counter.values()) or 1
        cumplidos = cumplimiento_counter.get(EstadoCumplimiento.CUMPLIDO, 0)
        base = cumplidos / total * 100
        penalizacion = incidentes_counter.get(SeveridadIncidente.CRITICA, 0) * 15 + incidentes_counter.get(SeveridadIncidente.ALTA, 0) * 8
        return max(base - penalizacion, 0.0)

    def _risk_level(self, score: float, incidentes_counter: Counter) -> str:
        if score >= 80 and incidentes_counter.get(SeveridadIncidente.ALTA, 0) == 0:
            return "bajo"
        if score >= 50:
            return "medio"
        return "alto"

    def render_summary(self, resumen: dict[str, Any]) -> str:
        return (
            "Nivel de riesgo: {riesgo}. Puntaje global: {score:.1f}. "
            "Cumplimientos: {cumplimientos}. Incidentes: {incidentes}."
        ).format(**resumen)