# Contratos de la API

## Autenticación
- `POST /api/v1/auth/register`: registra un usuario.
- `POST /api/v1/auth/login`: devuelve token pseudo-JWT.
- `GET /api/v1/auth/users`: lista usuarios.

## Empresas
- `POST /api/v1/empresas`: crea una empresa.
- `GET /api/v1/empresas`: lista empresas.
- `GET /api/v1/empresas/{id}`: detalle de empresa.
- `PATCH /api/v1/empresas/{id}`: actualización parcial.

## Suscripciones
- `POST /api/v1/suscripciones`: crea una suscripción y registra un pago.
- `POST /api/v1/suscripciones/{id}/cancel`: cancela la suscripción.
- `POST /api/v1/suscripciones/{id}/renew`: renueva la suscripción.
- `GET /api/v1/suscripciones`: lista suscripciones.

## Reportes
- `POST /api/v1/reportes/{empresa_id}`: genera un reporte.
- `GET /api/v1/reportes`: lista reportes.
- `GET /api/v1/reportes/{empresa_id}/export`: exporta contexto y payload SUT.

## IA y cumplimiento
- `GET /api/v1/auditor/{empresa_id}/resumen`: resumen de cumplimiento.
- `GET /api/v1/ia/{empresa_id}/analisis`: riesgo y recomendaciones.
- `GET /api/v1/tecnico/{empresa_id}/incidentes`: incidentes registrados.
- `GET /api/v1/admin/overview`: métricas generales.

## Documentos PDF
- `GET /api/v1/archivos/pdf`: lista documentos.
- `POST /api/v1/archivos/pdf`: sube un PDF.
- `GET /api/v1/archivos/pdf/{id}`: devuelve metadata.
- `GET /api/v1/archivos/pdf/{id}/historial`: historial del documento.

Adicionalmente, los endpoints en `app/main.py` permiten descargar PDFs y acceder al visor HTML.