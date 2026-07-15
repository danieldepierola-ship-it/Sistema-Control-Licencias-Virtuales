from .excepciones import ErrorSistemaLicencias
from .formulario_cliente import formulario_registrar_cliente
from .formulario_consultas import (
    formulario_buscar_licencias_por_sku,
    formulario_listar_por_estado,
)
from .formulario_licencia import (
    formulario_anular_licencia,
    formulario_registrar_licencia,
    formulario_vender_licencia,
)
from .formulario_producto import formulario_registrar_producto
from .reporte_strategy import (
    ReportePorProductoStrategy,
    ReporteStockStrategy,
)
from .sistema_licencias import SistemaLicencias
from .entradas import pausar


def menu():
    sistema = SistemaLicencias()

    while True:
        print("\n==========================================")
        print(" SISTEMA DE CONTROL DE LICENCIAS VIRTUALES")
        print(" ESET PERÚ")
        print("==========================================")
        print("1. Registrar licencia virtual-ESD")
        print("2. Registrar producto y costo")
        print("3. Registrar proveedor y descuento")
        print("4. Buscar licencias por SKU")
        print("5. Asignación y venta de licencias")
        print("6. Verificar licencias por estado")
        print("7. Anular licencia vendida")
        print("8. Reporte de stock, ventas y devoluciones")
        print("9. Reporte valorizado por producto")
        print("10. Salir")

        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                formulario_registrar_licencia(sistema)

            elif opcion == "2":
                formulario_registrar_producto(sistema)

            elif opcion == "3":
                formulario_registrar_cliente(sistema)

            elif opcion == "4":
                formulario_buscar_licencias_por_sku(sistema)

            elif opcion == "5":
                formulario_vender_licencia(sistema)

            elif opcion == "6":
                formulario_listar_por_estado(sistema)

            elif opcion == "7":
                formulario_anular_licencia(sistema)

            elif opcion == "8":
                sistema.configurar_reporte(ReporteStockStrategy())
                print("\n" + sistema.generar_reporte())

            elif opcion == "9":
                sistema.configurar_reporte(ReportePorProductoStrategy())
                print("\n" + sistema.generar_reporte())

            elif opcion == "10":
                print("Saliendo del sistema...")
                break

            else:
                print(
                    "Opción no válida. "
                    "Seleccione una opción del 1 al 10."
                )
                continue

        except ErrorSistemaLicencias as error:
            print(f"Error controlado: {error}")

        except Exception as error:
            print(f"Error inesperado controlado: {error}")

        pausar()


if __name__ == "__main__":
    menu()
