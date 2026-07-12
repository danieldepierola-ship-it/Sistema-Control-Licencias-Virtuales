from .entradas import (
    solicitar_decimal_positivo,
    solicitar_entero_positivo,
    solicitar_texto,
)
from .sistema_licencias import SistemaLicencias

def formulario_registrar_producto(
    sistema: SistemaLicencias,
):
    print("\nREGISTRO DE PRODUCTO")
    print("Precios en dólares y sin IGV.")
    print("Escriba Y para regresar.")

    while True:
        sku = solicitar_texto(
            "SKU: ",
            "SKU",
        )

        if sku is None:
            return

        sku = sku.upper()

        if sistema.buscar_producto_por_sku(sku) is not None:
            print(
                f"Error: ya existe un producto con el SKU '{sku}'."
            )
            continue

        break

    nombre = solicitar_texto(
        "Nombre del producto: ",
        "nombre del producto",
    )

    if nombre is None:
        return

    duracion = solicitar_entero_positivo(
        "Duración en meses: ",
        "duración en meses",
    )

    if duracion is None:
        return

    equipos = solicitar_entero_positivo(
        "Cantidad de equipos: ",
        "cantidad de equipos",
    )

    if equipos is None:
        return

    costo = solicitar_decimal_positivo(
        "Costo fijo sin IGV (USD): ",
        "costo sin IGV",
    )

    if costo is None:
        return

    producto = sistema.registrar_producto(
        sku,
        nombre,
        duracion,
        equipos,
        costo,
    )

    print("Producto registrado correctamente.")
    print(producto.mostrar_datos_completos())
