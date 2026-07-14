from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from decimal import Decimal
from typing import Iterable

from .licencia_virtual import LicenciaVirtual
from .validaciones import moneda

class ReporteStrategy(ABC):
    @abstractmethod
    def generar(
        self,
        licencias: Iterable[LicenciaVirtual],
    ) -> str:
        pass

class ReporteStockStrategy(ReporteStrategy):
    def generar(
        self,
        licencias: Iterable[LicenciaVirtual],
    ) -> str:
        licencias = list(
            licencias
        )

        conteo_actual = Counter(
            licencia.estado
            for licencia in licencias
        )

        stock_libre_valorizado = sum(
            (
                licencia.producto.costo_sin_igv_usd
                for licencia in licencias
                if licencia.estado == "Disponible"
            ),
            Decimal("0.00"),
        )

        ventas_historicas = [
            licencia
            for licencia in licencias
            if licencia.venta_realizada
        ]

        venta_bruta_historica = sum(
            (
                licencia.monto_venta_usd
                or Decimal("0.00")
                for licencia in ventas_historicas
            ),
            Decimal("0.00"),
        )

        devoluciones = sum(
            (
                licencia.monto_devolucion_usd
                for licencia in licencias
                if licencia.estado == "Anulada"
            ),
            Decimal("0.00"),
        )

        venta_neta = (
            venta_bruta_historica - devoluciones
        )

        return (
            "REPORTE GENERAL DE STOCK Y VENTAS\n"
            "----------------------------------\n"
            f"Total de licencias: {len(licencias)}\n"
            f"Disponibles actuales: "
            f"{conteo_actual['Disponible']}\n"
            f"Vendidas activas: "
            f"{conteo_actual['Vendida']}\n"
            f"Anuladas actuales: "
            f"{conteo_actual['Anulada']}\n"
            f"Ventas históricas realizadas: "
            f"{len(ventas_historicas)}\n"
            f"Stock libre valorizado: "
            f"{moneda(stock_libre_valorizado)}\n"
            f"Venta bruta histórica: "
            f"{moneda(venta_bruta_historica)}\n"
            f"Devoluciones: "
            f"{moneda(-devoluciones)}\n"
            f"Venta neta: "
            f"{moneda(venta_neta)}"
        )

class ReportePorProductoStrategy(ReporteStrategy):
    def generar(
        self,
        licencias: Iterable[LicenciaVirtual],
    ) -> str:
        agrupadas = defaultdict(
            list
        )

        for licencia in licencias:
            agrupadas[
                licencia.producto.sku
            ].append(
                licencia
            )

        if not agrupadas:
            return "No existen licencias registradas."

        lineas = [
            "REPORTE VALORIZADO POR PRODUCTO",
            "-------------------------------",
        ]

        for sku, lista in sorted(
            agrupadas.items()
        ):
            conteo_actual = Counter(
                licencia.estado
                for licencia in lista
            )

            ventas_historicas = [
                licencia
                for licencia in lista
                if licencia.venta_realizada
            ]

            venta_bruta = sum(
                (
                    licencia.monto_venta_usd
                    or Decimal("0.00")
                    for licencia in ventas_historicas
                ),
                Decimal("0.00"),
            )

            devoluciones = sum(
                (
                    licencia.monto_devolucion_usd
                    for licencia in lista
                    if licencia.estado == "Anulada"
                ),
                Decimal("0.00"),
            )

            venta_neta = (
                venta_bruta - devoluciones
            )

            producto = lista[0].producto

            lineas.append(
                f"{sku} - {producto.nombre}: "
                f"total={len(lista)}, "
                f"disponibles={conteo_actual['Disponible']}, "
                f"vendidas={len(ventas_historicas)}, "
                f"vendidas activas={conteo_actual['Vendida']}, "
                f"anuladas={conteo_actual['Anulada']}, "
                f"venta bruta={moneda(venta_bruta)}, "
                f"devoluciones={moneda(-devoluciones)}, "
                f"venta neta={moneda(venta_neta)}"
            )

        return "\n".join(
            lineas
        )
