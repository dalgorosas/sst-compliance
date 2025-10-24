# Herramientas de desarrollo

- `uvicorn app.main:app --reload` para levantar el servidor.
- `alembic` puede inicializarse en `app/db/migrations` si se requiere versionar la base de datos.
- Ejecutar pruebas rápidas: `pytest`.
- Revisar dependencias: `pip list --outdated`.

Recuerde que los archivos de PDF.js (`app/frontend/viewer/pdfjs/`) permanecen vacíos para ser completados manualmente.