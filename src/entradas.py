from .excepciones import ErrorSistemaLicencias
from .validaciones import (
    validar_correo,
    validar_decimal_positivo,
    validar_entero_positivo,
    validar_fecha,
    validar_porcentaje,
    validar_texto,
)

def solicitar_texto(
    mensaje: str,
    nombre_campo: str,
):
    while True:
        dato = input(mensaje).strip()

        if dato.upper() == "Y":
            return None

        try:
            return validar_texto(
                dato,
                nombre_campo,
            )

        except ErrorSistemaLicencias as error:
            print(f"Error: {error}")
            print(
                "Intente nuevamente o escriba Y para regresar."
            )

def solicitar_entero_positivo(
    mensaje: str,
    nombre_campo: str,
):
    while True:
        dato = input(mensaje).strip()

        if dato.upper() == "Y":
            return None

        try:
            return validar_entero_positivo(
                dato,
                nombre_campo,
            )

        except ErrorSistemaLicencias as error:
            print(f"Error: {error}")

def solicitar_decimal_positivo(
    mensaje: str,
    nombre_campo: str,
):
    while True:
        dato = input(mensaje).strip()

        if dato.upper() == "Y":
            return None

        try:
            return validar_decimal_positivo(
                dato,
                nombre_campo,
            )

        except ErrorSistemaLicencias as error:
            print(f"Error: {error}")

def solicitar_porcentaje(mensaje: str):
    while True:
        dato = input(mensaje).strip()

        if dato.upper() == "Y":
            return None

        try:
            return validar_porcentaje(
                dato
            )

        except ErrorSistemaLicencias as error:
            print(f"Error: {error}")

def solicitar_correo(mensaje: str):
    while True:
        dato = input(mensaje).strip()

        if dato.upper() == "Y":
            return None

        try:
            return validar_correo(
                dato
            )

        except ErrorSistemaLicencias as error:
            print(f"Error: {error}")

def solicitar_fecha(mensaje: str):
    while True:
        dato = input(mensaje).strip()

        if dato.upper() == "Y":
            return None

        try:
            fecha_normalizada = validar_fecha(
                dato
            )

            if dato != fecha_normalizada:
                print(
                    f"Fecha registrada como: {fecha_normalizada}"
                )

            return fecha_normalizada

        except ErrorSistemaLicencias as error:
            print(f"Error: {error}")

def confirmar(mensaje: str) -> bool:
    while True:
        respuesta = input(
            f"{mensaje} (S/N): "
        ).strip().upper()

        if respuesta == "S":
            return True

        if respuesta == "N":
            return False

        print(
            "Ingrese S para confirmar o N para cancelar."
        )

def pausar():
    input(
        "\nPresione ENTER para regresar al menú principal..."
    )
