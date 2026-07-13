from .entradas import (
    solicitar_correo,
    solicitar_porcentaje,
    solicitar_texto,
)
from .sistema_licencias import SistemaLicencias

def formulario_registrar_cliente(
    sistema: SistemaLicencias,
):
    print("\nREGISTRO DE MAYORISTA / CANAL")
    print("Escriba Y para regresar.")

    while True:
        print("1. Mayorista")
        print("2. Canal de venta")

        tipo = input(
            "Seleccione tipo de cliente: "
        ).strip()

        if tipo.upper() == "Y":
            return

        if tipo in {"1", "2"}:
            break

        print("Error: seleccione 1 o 2.")

    while True:
        documento = solicitar_texto(
            "RUC o documento: ",
            "documento",
        )

        if documento is None:
            return

        if sistema.buscar_cliente_por_documento(
            documento
        ) is not None:
            print(
                f"Error: ya existe un cliente con el documento "
                f"'{documento}'."
            )
            continue

        break

    nombre = solicitar_texto(
        "Razón social o nombre comercial: ",
        "nombre",
    )

    if nombre is None:
        return

    correo = solicitar_correo(
        "Correo de contacto: "
    )

    if correo is None:
        return

    telefono = solicitar_texto(
        "Teléfono de contacto: ",
        "teléfono",
    )

    if telefono is None:
        return

    descuento = solicitar_porcentaje(
        "Descuento comercial (%): "
    )

    if descuento is None:
        return

    cliente = sistema.registrar_cliente(
        tipo,
        documento,
        nombre,
        correo,
        telefono,
        descuento,
    )

    print("Cliente registrado correctamente.")
    print(cliente.mostrar_datos())
