from app.db.session import Base  # noqa

# Importar todos los modelos para registrar las clases en el mapper de SQLAlchemy
from app.models.user import User  # noqa
from app.models.empresa import Empresa  # noqa
from app.models.suscripcion import Suscripcion  # noqa
from app.models.pago import Pago  # noqa
from app.models.reporte import Reporte  # noqa
from app.models.cumplimiento import Cumplimiento  # noqa
from app.models.incidente import Incidente  # noqa
from app.models.auditoria import Auditoria  # noqa
from app.models.documento import Documento, DocumentoHistorial  # noqa