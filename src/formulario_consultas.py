from decimal import Decimal

from .entradas import solicitar_texto
from .excepciones import EntidadNoEncontradaError
from .sistema_licencias import SistemaLicencias
from .validaciones import moneda

def formulario_buscar_licencias_por_sku(
    sistema: SistemaLicencias,
):
    print("\nBÚSQUEDA DE LICENCIAS POR SKU")
    print("Escriba Y para regresar.")

    while True:
        sku = solicitar_texto(
            "Ingrese el SKU del producto: ",
            "SKU",
        )

        if sku is None:
            return

        try:
            licencias = sistema.buscar_licencias_por_sku(
                sku
            )
            break

        except EntidadNoEncontradaError as error:
            print(f"Error: {error}")

    producto = sistema.buscar_producto_por_sku(
        sku
    )

    print("\nPRODUCTO ENCONTRADO")
    print(producto.mostrar_datos_sin_precio())

    print(
        f"Cantidad de licencias asociadas: {len(licencias)}"
    )

    if not licencias:
        print(
            "Este producto todavía no tiene licencias registradas."
        )
        return

    print("\nLICENCIAS ASOCIADAS")

    for numero, licencia in enumerate(
        licencias,
        start=1,
    ):
        print(
            f"{numero}. {licencia.mostrar_datos_basicos_busqueda()}"
        )

def formulario_listar_por_estado(
    sistema: SistemaLicencias,
):
    print("\nVERIFICAR LICENCIAS POR ESTADO")
    print("1. Disponibles")
    print("2. Vendidas")
    print("3. Anuladas")
    print("Y. Regresar")

    while True:
        opcion = input(
            "Seleccione una opción: "
        ).strip().upper()

        if opcion == "Y":
            return

        mapa = {
            "1": "Disponible",
            "2": "Vendida",
            "3": "Anulada",
        }

        if opcion in mapa:
            estado = mapa[opcion]
            break

        print("Opción no válida.")

    if estado == "Vendida":
        # Se muestran todas las ventas históricas, aunque luego hayan sido anuladas.
        licencias = [
            licencia
            for licencia in sistema.licencias
            if licencia.venta_realizada
        ]
    else:
        licencias = sistema.listar_licencias_por_estado(
            estado
        )

    if not licencias:
        if estado == "Vendida":
            print("No existen ventas registradas.")
        else:
            print(
                f"No existen licencias en estado {estado}."
            )
        return

    if estado == "Vendida":
        print(
            f"\nCantidad de ventas históricas registradas: "
            f"{len(licencias)}"
        )
    else:
        print(
            f"\nCantidad de licencias en estado "
            f"{estado}: {len(licencias)}"
        )

    if estado == "Disponible":
        for numero, licencia in enumerate(
            licencias,
            start=1,
        ):
            print(
                f"{numero}. {licencia.mostrar_datos_disponible()}"
            )

    elif estado == "Vendida":
        total = Decimal("0.00")

        for numero, licencia in enumerate(
            licencias,
            start=1,
        ):
            indicador = (
                " (ANULADA)"
                if licencia.estado == "Anulada"
                else ""
            )

            print(
                f"{numero}. {licencia.mostrar_datos_venta()}"
                f"{indicador}"
            )

            total += (
                licencia.monto_venta_usd
                or Decimal("0.00")
            )

        print(
            "\nTOTAL HISTÓRICO DE VENTAS: "
            f"{moneda(total)}"
        )

    elif estado == "Anulada":
        total_devoluciones = Decimal(
            "0.00"
        )

        for numero, licencia in enumerate(
            licencias,
            start=1,
        ):
            print(
                f"{numero}. {licencia.mostrar_datos_anulacion()}"
            )

            total_devoluciones += (
                licencia.monto_devolucion_usd
            )

        if total_devoluciones > 0:
            print(
                "\nTOTAL DEVUELTO: "
                f"{moneda(-total_devoluciones)}"
            )
