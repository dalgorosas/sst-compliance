"""Tipos utilitarios para los esquemas Pydantic.

Evita dependencias opcionales como :mod:`email_validator` proporcionando un tipo
de email basado en validación por expresión regular.  Esto permite ejecutar las
pruebas automatizadas sin instalar paquetes adicionales mientras mantenemos una
validación básica de formato.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import StringConstraints

# Patrón minimalista para validar correos electrónicos.  No pretende cubrir el
# estándar completo de RFC 5322, pero sirve para la mayoría de los usos sin
# requerir ``email-validator``.
EmailStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=3,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
    ),
]
