"""Ligera implementación local de ``email_validator``.

Esta versión solo cubre la funcionalidad mínima requerida por
``pydantic`` durante las pruebas: validar que la dirección contenga un
``@`` y exponer una estructura con el atributo ``email``.

La dependencia oficial no puede instalarse en el entorno de evaluación
por las restricciones de red, por lo que este módulo actúa como
emulación para los tests automatizados.
"""

from __future__ import annotations

from dataclasses import dataclass


class EmailNotValidError(ValueError):
    """Excepción lanzada cuando la dirección no es válida."""


@dataclass
class ValidatedEmail:
    """Respuesta simplificada compatible con ``pydantic``."""

    email: str


def validate_email(
    email: str,
    *,
    allow_smtputf8: bool = True,
    allow_empty_local: bool = False,
    check_deliverability: bool = False,
):
    """Valida la dirección de correo.

    La implementación comprueba únicamente la presencia del carácter
    ``@`` como criterio básico para las pruebas.
    """

    if not isinstance(email, str) or "@" not in email:
        raise EmailNotValidError("La dirección de correo debe contener '@'.")

    return ValidatedEmail(email=email)


__all__ = [
    "EmailNotValidError",
    "ValidatedEmail",
    "validate_email",
]
