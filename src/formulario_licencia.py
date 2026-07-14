from .entradas import confirmar, solicitar_fecha, solicitar_texto
from .sistema_licencias import SistemaLicencias

def formulario_registrar_licencia(
    sistema: SistemaLicencias,
):
    print("\nREGISTRO DE LICENCIA VIRTUAL")
    print("Escriba Y para regresar.")

    if not sistema.productos:
        print(
            "Primero debe registrar al menos un producto."
        )
        return

    while True:
        codigo = solicitar_texto(
            "Código de licencia: ",
            "código de licencia",
        )

        if codigo is None:
            return

        codigo = codigo.upper()

        if sistema.buscar_licencia_por_codigo(
            codigo
        ) is not None:
            print(
                f"Error: ya existe una licencia con el código "
                f"'{codigo}'."
            )
            continue

        break

    print("\nPRODUCTOS REGISTRADOS")

    for producto in sistema.productos:
        print(
            producto.mostrar_datos_sin_precio()
        )

    while True:
        sku = solicitar_texto(
            "SKU del producto asociado: ",
            "SKU",
        )

        if sku is None:
            return

        sku = sku.upper()

        if sistema.buscar_producto_por_sku(
            sku
        ) is None:
            print(
                f"Error: no existe un producto con el SKU '{sku}'."
            )
            continue

        break

    fecha = solicitar_fecha(
        "Fecha de ingreso (DD/MM/AAAA o DD/MM/AA): "
    )

    if fecha is None:
        return

    licencia = sistema.registrar_licencia(
        codigo,
        sku,
        fecha,
    )

    print("Licencia registrada correctamente.")
    print(licencia.mostrar_datos_disponible())

def formulario_vender_licencia(
    sistema: SistemaLicencias,
):
    print("\nASIGNAR / VENDER LICENCIA")
    print(
        "Al asignar la licencia, la venta queda registrada."
    )
    print("Escriba Y para regresar.")

    while True:
        codigo = solicitar_texto(
            "Código de licencia: ",
            "código de licencia",
        )

        if codigo is None:
            return

        licencia = sistema.buscar_licencia_por_codigo(
            codigo
        )

        if licencia is None:
            print(
                f"Error: no existe la licencia '{codigo}'."
            )
            continue

        if licencia.estado != "Disponible":
            print(
                f"Error: la licencia está en estado "
                f"'{licencia.estado}'."
            )
            continue

        break

    while True:
        documento = solicitar_texto(
            "Documento del cliente: ",
            "documento del cliente",
        )

        if documento is None:
            return

        cliente = sistema.buscar_cliente_por_documento(
            documento
        )

        if cliente is None:
            print(
                f"Error: no existe el cliente '{documento}'."
            )
            continue

        break

    licencia = sistema.vender_licencia(
        codigo,
        documento,
    )

    print("Licencia asignada y vendida correctamente.")
    print(licencia.mostrar_datos_basicos_busqueda())

def formulario_anular_licencia(
    sistema: SistemaLicencias,
):
    print("\nANULAR LICENCIA VENDIDA")
    print(
        "Solo se pueden anular licencias previamente vendidas."
    )
    print("Escriba Y para regresar.")

    while True:
        codigo = solicitar_texto(
            "Código de licencia vendida: ",
            "código de licencia",
        )

        if codigo is None:
            return

        licencia = sistema.buscar_licencia_por_codigo(
            codigo
        )

        if licencia is None:
            print(
                f"Error: no existe la licencia '{codigo}'."
            )
            continue

        if licencia.estado != "Vendida":
            print(
                f"Error: la licencia está en estado "
                f"'{licencia.estado}' y no puede anularse."
            )
            continue

        break

    print("\nLICENCIA VENDIDA SELECCIONADA")
    print(licencia.mostrar_datos_venta())

    print("\nTIPO DE ANULACIÓN")
    print("1. Sin devolución")
    print(
        "   Ejemplo: falla técnica, cambio por garantía."
    )
    print("2. Con devolución")
    print(
        "   Ejemplo: cancelación comercial del cliente."
    )

    while True:
        tipo = input(
            "Seleccione 1 o 2: "
        ).strip()

        if tipo.upper() == "Y":
            return

        if tipo in {"1", "2"}:
            break

        print("Opción no válida.")

    con_devolucion = (
        tipo == "2"
    )

    motivo = solicitar_texto(
        "Ingrese el motivo de la anulación: ",
        "motivo de anulación",
    )

    if motivo is None:
        return

    if not confirmar(
        "¿Confirmar anulación definitiva?"
    ):
        return

    sistema.anular_licencia(
        codigo,
        motivo,
        con_devolucion,
    )

    print("Licencia anulada correctamente.")
    print(licencia.mostrar_datos_anulacion())
    print("\n" + licencia.mostrar_historial())
