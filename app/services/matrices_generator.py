from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from app.models.cumplimiento import Cumplimiento
from app.models.incidente import Incidente, SeveridadIncidente


class MatricesGenerator:
    def compliance_matrix(
        self,
        cumplimientos: Iterable[Cumplimiento],
        incidentes: Iterable[Incidente],
    ) -> list[dict[str, str]]:
        matrix = []
        incidentes_por_severidad = self._incidentes_por_severidad(incidentes)
        for item in cumplimientos:
            matrix.append(
                {
                    "normativa": item.normativa,
                    "requisito": item.requisito,
                    "estado": item.estado.value,
                    "incidentes_alta": str(incidentes_por_severidad[SeveridadIncidente.ALTA]),
                    "incidentes_critica": str(incidentes_por_severidad[SeveridadIncidente.CRITICA]),
                }
            )
        return matrix

    def _incidentes_por_severidad(self, incidentes: Iterable[Incidente]):
        counter = defaultdict(int)
        for incidente in incidentes:
            counter[incidente.severidad] += 1
        for level in SeveridadIncidente:
            counter.setdefault(level, 0)
        return counter