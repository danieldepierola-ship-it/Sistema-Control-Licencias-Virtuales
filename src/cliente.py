from abc import ABC, abstractmethod
from decimal import Decimal

from .validaciones import (
    validar_correo,
    validar_porcentaje,
    validar_texto,
)

class Cliente(ABC):
    def __init__(self, documento: str, nombre: str, correo: str, telefono: str):
        self.documento = validar_texto(
            documento,
            "documento",
        )

        self.nombre = validar_texto(
            nombre,
            "nombre",
        )

        self.correo = validar_correo(
            correo
        )
        self.telefono = validar_texto(telefono,"teléfono")

    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def obtener_descuento(self) -> Decimal:
        pass

    def calcular_precio_venta(
        self,
        costo_base: Decimal,
    ) -> Decimal:
        descuento = self.obtener_descuento()

        factor = Decimal("1") - (
            descuento / Decimal("100")
        )

        return (
            costo_base * factor
        ).quantize(
            DOS_DECIMALES,
            rounding=ROUND_HALF_UP,
        )

    def mostrar_datos(self) -> str:
        return (
            f"Documento: {self.documento} | "
            f"Nombre: {self.nombre} | "
            f"Correo: {self.correo} | Teléfono: {self.telefono} | "
            f"Tipo: {self.tipo}"
        )

class Mayorista(Cliente):
    def __init__(self, documento, nombre, correo, telefono, descuento):
        super().__init__(
            documento,
            nombre,
            correo,
            telefono,
        )

        self.descuento = validar_porcentaje(
            descuento
        )

    @property
    def tipo(self) -> str:
        return "Mayorista"

    def obtener_descuento(self) -> Decimal:
        return self.descuento

    def mostrar_datos(self) -> str:
        return (
            super().mostrar_datos()
            + f" | Descuento: {self.descuento}%"
        )

class CanalVenta(Cliente):
    def __init__(
        self,
        documento,
        nombre,
        correo,
        telefono,
        descuento,
    ):
        super().__init__(
            documento,
            nombre,
            correo,
            telefono,
        )

        self.descuento = validar_porcentaje(
            descuento
        )

    @property
    def tipo(self) -> str:
        return "Canal de Venta"

    def obtener_descuento(self) -> Decimal:
        return self.descuento

    def mostrar_datos(self) -> str:
        return (
            super().mostrar_datos()
            + f" | Descuento: {self.descuento}%"
        )
