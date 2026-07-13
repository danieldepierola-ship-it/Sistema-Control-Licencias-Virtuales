from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional

from .cliente import Cliente
from .excepciones import EstadoLicenciaError
from .producto import Producto
from .validaciones import (
    fecha_hora_actual,
    moneda,
    validar_fecha,
    validar_texto,
)

class LicenciaVirtual:
    ESTADOS_VALIDOS = {
        "Disponible",
        "Vendida",
        "Anulada",
    }

    codigo_licencia: str
    producto: Producto
    fecha_ingreso: str

    estado: str = field(
        default="Disponible"
    )

    cliente_asignado: Optional[Cliente] = field(
        default=None
    )

    fecha_venta: Optional[str] = field(
        default=None
    )

    monto_venta_usd: Optional[Decimal] = field(
        default=None
    )

    descuento_aplicado: Optional[Decimal] = field(
        default=None
    )

    venta_realizada: bool = field(
        default=False
    )

    motivo_anulacion: Optional[str] = field(
        default=None
    )

    tipo_anulacion: Optional[str] = field(
        default=None
    )

    monto_devolucion_usd: Decimal = field(
        default=Decimal("0.00")
    )

    ultimo_cliente: Optional[str] = field(
        default=None
    )

    historial: List[str] = field(
        default_factory=list
    )

    def __post_init__(self):
        self.codigo_licencia = validar_texto(
            self.codigo_licencia,
            "código de licencia",
        ).upper()

        self.fecha_ingreso = validar_fecha(
            self.fecha_ingreso
        )

        if self.estado not in self.ESTADOS_VALIDOS:
            raise EstadoLicenciaError(
                f"Estado no válido: {self.estado}"
            )

        self.registrar_historial(
            "Licencia registrada como Disponible."
        )

    def registrar_historial(
        self,
        descripcion: str,
    ) -> None:
        self.historial.append(
            f"{fecha_hora_actual()} - {descripcion}"
        )

    def vender_a(
        self,
        cliente: Cliente,
    ) -> None:
        if self.estado != "Disponible":
            raise EstadoLicenciaError(
                "Solo se puede vender una licencia disponible."
            )

        self.cliente_asignado = cliente
        self.ultimo_cliente = cliente.nombre

        self.descuento_aplicado = (
            cliente.obtener_descuento()
        )

        self.monto_venta_usd = (
            cliente.calcular_precio_venta(
                self.producto.costo_sin_igv_usd
            )
        )

        self.fecha_venta = fecha_hora_actual()
        self.venta_realizada = True
        self.estado = "Vendida"

        self.registrar_historial(
            f"Licencia vendida/asignada a {cliente.nombre} "
            f"({cliente.documento}). "
            f"Monto: {moneda(self.monto_venta_usd)}."
        )

    def anular(
        self,
        motivo: str,
        con_devolucion: bool,
    ) -> None:
        if self.estado == "Anulada":
            raise EstadoLicenciaError(
                "La licencia ya está anulada."
            )

        if self.estado != "Vendida":
            raise EstadoLicenciaError(
                "Solo se puede anular una licencia vendida."
            )

        motivo = validar_texto(
            motivo,
            "motivo de anulación",
        )

        if self.cliente_asignado is not None:
            self.ultimo_cliente = (
                self.cliente_asignado.nombre
            )

        self.motivo_anulacion = motivo

        if con_devolucion:
            self.tipo_anulacion = "Con devolución"

            self.monto_devolucion_usd = (
                self.monto_venta_usd
                or Decimal("0.00")
            )
        else:
            self.tipo_anulacion = "Sin devolución"

            self.monto_devolucion_usd = Decimal(
                "0.00"
            )

        self.cliente_asignado = None
        self.estado = "Anulada"

        self.registrar_historial(
            f"Licencia anulada. "
            f"Tipo: {self.tipo_anulacion}. "
            f"Motivo: {motivo}. "
            f"Devolución: {moneda(self.monto_devolucion_usd)}."
        )

    def mostrar_datos_disponible(self) -> str:
        return (
            f"Código: {self.codigo_licencia} | "
            f"Producto: {self.producto.nombre} | "
            f"SKU: {self.producto.sku} | "
            f"Fecha ingreso: {self.fecha_ingreso}"
        )

    def mostrar_datos_venta(self) -> str:
        cliente = (
            self.cliente_asignado.nombre
            if self.cliente_asignado is not None
            else self.ultimo_cliente or "Sin cliente"
        )

        return (
            f"Código: {self.codigo_licencia} | "
            f"Producto: {self.producto.nombre} | "
            f"SKU: {self.producto.sku} | "
            f"Cliente: {cliente} | "
            f"Fecha venta/asignación: {self.fecha_venta} | "
            f"Descuento: {self.descuento_aplicado}% | "
            f"Monto venta: {moneda(self.monto_venta_usd)}"
        )

    def mostrar_datos_basicos_busqueda(self) -> str:
        cliente = (
            self.cliente_asignado.nombre
            if self.cliente_asignado is not None
            else self.ultimo_cliente or "Sin asignar"
        )

        fecha_relevante = (
            self.fecha_venta
            if self.estado in {"Vendida", "Anulada"}
            else self.fecha_ingreso
        )

        etiqueta_fecha = (
            "Fecha venta/asignación"
            if self.estado in {"Vendida", "Anulada"}
            else "Fecha ingreso"
        )

        return (
            f"Código: {self.codigo_licencia} | "
            f"Producto: {self.producto.nombre} | "
            f"SKU: {self.producto.sku} | "
            f"Estado: {self.estado} | "
            f"{etiqueta_fecha}: {fecha_relevante} | "
            f"Cliente: {cliente}"
        )

    def mostrar_datos_anulacion(self) -> str:
        devolucion = (
            -self.monto_devolucion_usd
            if self.monto_devolucion_usd > 0
            else Decimal("0.00")
        )

        texto = (
            f"Código: {self.codigo_licencia} | "
            f"Producto: {self.producto.nombre} | "
            f"SKU: {self.producto.sku} | "
            f"Venta original: {self.fecha_venta} | "
            f"Último cliente: "
            f"{self.ultimo_cliente or 'Sin cliente'} | "
            f"Tipo: {self.tipo_anulacion} | "
            f"Motivo: {self.motivo_anulacion}"
        )

        if self.tipo_anulacion == "Con devolución":
            texto += (
                f" | Devolución: {moneda(devolucion)}"
            )

        return texto

    def mostrar_historial(self) -> str:
        lineas = [
            f"HISTORIAL DE {self.codigo_licencia}",
            "--------------------------------",
        ]

        lineas.extend(
            self.historial
        )

        return "\n".join(
            lineas
        )
