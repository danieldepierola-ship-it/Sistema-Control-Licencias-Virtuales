from dataclasses import dataclass
from decimal import Decimal

from .validaciones import (
    moneda,
    validar_decimal_positivo,
    validar_entero_positivo,
    validar_texto,
)
print("holamundo")
class Producto:
    sku: str
    nombre: str
    duracion_meses: int
    cantidad_equipos: int
    costo_sin_igv_usd: Decimal

    def __post_init__(self):
        self.sku = validar_texto(
            self.sku,
            "SKU",
        ).upper()

        self.nombre = validar_texto(
            self.nombre,
            "nombre del producto",
        )

        self.duracion_meses = validar_entero_positivo(
            self.duracion_meses,
            "duración en meses",
        )

        self.cantidad_equipos = validar_entero_positivo(
            self.cantidad_equipos,
            "cantidad de equipos",
        )

        self.costo_sin_igv_usd = validar_decimal_positivo(
            self.costo_sin_igv_usd,
            "costo sin IGV",
        )

    def mostrar_datos_completos(self) -> str:
        return (
            f"SKU: {self.sku} | "
            f"Producto: {self.nombre} | "
            f"Duración: {self.duracion_meses} meses | "
            f"Equipos: {self.cantidad_equipos} | "
            f"Costo base sin IGV: {moneda(self.costo_sin_igv_usd)}"
        )

    def mostrar_datos_sin_precio(self) -> str:
        return (
            f"SKU: {self.sku} | "
            f"Producto: {self.nombre} | "
            f"Duración: {self.duracion_meses} meses | "
            f"Equipos: {self.cantidad_equipos}"
        )
