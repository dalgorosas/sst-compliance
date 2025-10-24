# Arquitectura de SST Compliance

La plataforma está estructurada en capas para favorecer la separación de responsabilidades:

## Capa de presentación
- **FastAPI** expone routers versionados ubicados en `app/api/v1/`.
- El archivo `app/main.py` construye la aplicación (`create_app`) e incorpora endpoints auxiliares para la gestión de PDFs y el visor web.
- El frontend embebido (`app/frontend/`) contiene un visor PDF básico apoyado en PDF.js (archivos `pdf.js` y `pdf.worker.js` permanecen vacíos para completarse posteriormente).

## Capa de servicios
- Los servicios dentro de `app/services/` encapsulan la lógica de dominio: motor de cumplimiento, generación de reportes, exportaciones SUT, gestión de suscripciones y procesamientos simulados de pagos.
- Cada servicio se apoya en repositorios (`app/repositories/`) que abstraen el acceso a la base de datos.

## Persistencia
- SQLAlchemy 2.0 define los modelos (`app/models/`) y `app/db/session.py` provee la sesión y el motor.
- Los repositorios heredan de `BaseRepo` y exponen operaciones CRUD típicas.

## Infraestructura y utilidades
- `app/core/` concentra la configuración, seguridad y manejo de eventos del ciclo de vida de FastAPI.
- `app/tasks/` registra tareas programadas simples mediante `threading.Timer`.
- `app/utils/` ofrece herramientas auxiliares (validaciones, hash, manejo de archivos y zonas horarias).

## Flujo típico
1. Un usuario se registra (`/api/v1/auth/register`) y crea una empresa (`/api/v1/empresas`).
2. Se crea una suscripción (`/api/v1/suscripciones`) y se generan reportes (`/api/v1/reportes`).
3. Los servicios calculan métricas de cumplimiento, riesgos e incidentes, disponibles para administradores, auditores y técnicos.