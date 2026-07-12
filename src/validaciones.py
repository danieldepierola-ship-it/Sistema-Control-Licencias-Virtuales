import re
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import Optional

from .excepciones import CampoVacioError, DatoInvalidoError

DOS_DECIMALES = Decimal("0.01")

def moneda(valor: Optional[Decimal]) -> str:
    if valor is None:
        valor = Decimal("0.00")

    valor = valor.quantize(
        DOS_DECIMALES,
        rounding=ROUND_HALF_UP,
    )

    return f"USD {valor}"

def fecha_hora_actual() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def validar_texto(valor: str, nombre_campo: str) -> str:
    valor_limpio = str(valor).strip()

    if not valor_limpio:
        raise CampoVacioError(
            f"El campo '{nombre_campo}' no puede quedar vacío."
        )

    return valor_limpio

def validar_entero_positivo(valor, nombre_campo: str) -> int:
    try:
        numero = int(valor)
    except (TypeError, ValueError) as exc:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser un número entero."
        ) from exc

    if numero <= 0:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser mayor que cero."
        )

    return numero

def validar_decimal_no_negativo(valor, nombre_campo: str) -> Decimal:
    try:
        numero = Decimal(str(valor).strip())
    except (InvalidOperation, ValueError) as exc:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser numérico."
        ) from exc

    if numero < 0:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' no puede ser negativo."
        )

    return numero.quantize(
        DOS_DECIMALES,
        rounding=ROUND_HALF_UP,
    )

def validar_decimal_positivo(valor, nombre_campo: str) -> Decimal:
    numero = validar_decimal_no_negativo(
        valor,
        nombre_campo,
    )

    if numero <= 0:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe ser mayor que cero."
        )

    return numero

def validar_porcentaje(valor, nombre_campo: str = "descuento") -> Decimal:
    numero = validar_decimal_no_negativo(
        valor,
        nombre_campo,
    )

    if numero > 100:
        raise DatoInvalidoError(
            f"El campo '{nombre_campo}' debe estar entre 0 y 100."
        )

    return numero

def validar_correo(correo: str) -> str:
    correo = validar_texto(
        correo,
        "correo",
    )

    patron = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

    if not re.match(patron, correo):
        raise DatoInvalidoError(
            "El correo ingresado no tiene un formato válido."
        )

    return correo

def validar_fecha(fecha: str) -> str:
    fecha = validar_texto(
        fecha,
        "fecha de ingreso",
    )

    for formato in ("%d/%m/%Y", "%d/%m/%y"):
        try:
            fecha_convertida = datetime.strptime(
                fecha,
                formato,
            )

            if formato == "%d/%m/%y":
                partes = fecha.split("/")
                fecha_convertida = fecha_convertida.replace(
                    year=2000 + int(partes[2])
                )

            return fecha_convertida.strftime("%d/%m/%Y")

        except ValueError:
            continue

    raise DatoInvalidoError(
        "La fecha debe tener el formato DD/MM/AAAA o DD/MM/AA."
    )
