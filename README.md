# SST Compliance Platform

Este repositorio contiene una API construida con FastAPI que centraliza la gestión de normativas de Seguridad y Salud en el Trabajo (SST). El objetivo principal es ofrecer una base sólida para administrar empresas, usuarios, suscripciones, reportes y el ciclo de cumplimiento normativo.

## Características

- **API REST modular:** organizada por dominios (auth, empresas, reportes, IA, etc.) para facilitar la escalabilidad.
- **Persistencia con SQLAlchemy 2.0:** modelos relacionales con relaciones explícitas y repositorios reutilizables.
- **Servicios de negocio:** capa de servicios que concentra la lógica de cumplimiento, generación de reportes y automatizaciones.
- **Gestión de documentos PDF:** almacenamiento de archivos y visualización mediante un visor basado en PDF.js.
- **Tareas programables:** infraestructura ligera para disparar trabajos periódicos (recordatorios, generación de reportes, etc.).

## Requisitos

- Python 3.11+
- Dependencias listadas en `pyproject.toml`

## Puesta en marcha

```bash
pip install -e .
uvicorn app.main:app --reload
```

La aplicación expone la documentación interactiva en `http://localhost:8000/docs` y el visor de PDF en `http://localhost:8000/view/{id}`.

## Estructura relevante

- `app/core`: configuración, seguridad y utilidades comunes.
- `app/models`: definición de tablas SQLAlchemy.
- `app/repositories`: capa de acceso a datos con operaciones CRUD.
- `app/services`: lógica de dominio reusable por los endpoints.
- `app/api`: routers versionados de FastAPI.
- `app/utils`: herramientas auxiliares para validaciones, archivos y fechas.

## Próximos pasos

Los archivos `app/frontend/viewer/pdfjs/pdf.js` y `app/frontend/viewer/pdfjs/pdf.worker.js` permanecen vacíos para que puedan ser completados con los recursos oficiales de PDF.js o diseñados manualmente posteriormente. Igualmente, los archivos de configuración `.json` que se creen deberán completarse según las necesidades del despliegue.