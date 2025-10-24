from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.reporte import Reporte
from app.repositories.cumplimiento_repo import CumplimientoRepo
from app.repositories.empresa_repo import EmpresaRepo
from app.repositories.incidente_repo import IncidenteRepo
from app.repositories.reporte_repo import ReporteRepo
from app.services.compliance_engine import ComplianceEngine
from app.services.matrices_generator import MatricesGenerator


class ReportBuilder:
    def __init__(
        self,
        report_repo: ReporteRepo | None = None,
        empresa_repo: EmpresaRepo | None = None,
        cumplimiento_repo: CumplimientoRepo | None = None,
        incidente_repo: IncidenteRepo | None = None,
    ) -> None:
        self.report_repo = report_repo or ReporteRepo()
        self.empresa_repo = empresa_repo or EmpresaRepo()
        self.cumplimiento_repo = cumplimiento_repo or CumplimientoRepo()
        self.incidente_repo = incidente_repo or IncidenteRepo()
        self.engine = ComplianceEngine()
        self.matrices = MatricesGenerator()

    def _build_context(self, db: Session, empresa_id: int) -> dict[str, Any]:
        empresa = self.empresa_repo.get(db, empresa_id)
        cumplimientos = self.cumplimiento_repo.por_empresa(db, empresa_id)
        incidentes = self.incidente_repo.por_empresa(db, empresa_id)
        resumen = self.engine.evaluate_company(cumplimientos, incidentes)
        matriz = self.matrices.compliance_matrix(cumplimientos, incidentes)
        return {
            "empresa": empresa,
            "cumplimientos": cumplimientos,
            "incidentes": incidentes,
            "resumen": resumen,
            "matriz": matriz,
        }

    def build_report(self, db: Session, empresa_id: int, generado_por: str = "sistema") -> Reporte:
        ctx = self._build_context(db, empresa_id)
        descripcion = self.engine.render_summary(ctx["resumen"])
        return self.report_repo.create(
            db,
            empresa_id=empresa_id,
            titulo=f"Reporte de cumplimiento {datetime.utcnow():%Y-%m-%d}",
            descripcion=descripcion,
            generado_por=generado_por,
        )

    def build_scheduled_reports(self) -> list[Reporte]:
        results: list[Reporte] = []
        with SessionLocal() as db:
            empresas = self.empresa_repo.list(db)
            for empresa in empresas:
                results.append(self.build_report(db, empresa.id))
        return results

    def export_context(self, db: Session, empresa_id: int) -> dict[str, Any]:
        ctx = self._build_context(db, empresa_id)
        from app.services.sut_exporter import SUTExporter

        exporter = SUTExporter()
        sut_payload = exporter.export(ctx["cumplimientos"], ctx["incidentes"])
        return {
            "empresa": {
                "id": ctx["empresa"].id,
                "nombre": ctx["empresa"].nombre,
            },
            "resumen": ctx["resumen"],
            "matriz": ctx["matriz"],
            "cumplimientos": [
                {
                    "id": cumplimiento.id,
                    "normativa": cumplimiento.normativa,
                    "requisito": cumplimiento.requisito,
                    "estado": cumplimiento.estado.value,
                }
                for cumplimiento in ctx["cumplimientos"]
            ],
            "incidentes": [
                {
                    "id": incidente.id,
                    "titulo": incidente.titulo,
                    "severidad": incidente.severidad.value,
                }
                for incidente in ctx["incidentes"]
            ],
            "sut": sut_payload,
        }