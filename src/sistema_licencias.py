from typing import List, Optional

from .cliente import Cliente
from .cliente_factory import ClienteFactory
from .excepciones import (
    EntidadDuplicadaError,
    EntidadNoEncontradaError,
    EstadoLicenciaError,
)
from .licencia_virtual import LicenciaVirtual
from .producto import Producto
from .reporte_strategy import ReporteStockStrategy, ReporteStrategy
from .validaciones import validar_texto

class SistemaLicencias:
    def __init__(self):
        self.productos: List[Producto] = []
        self.clientes: List[Cliente] = []
        self.licencias: List[LicenciaVirtual] = []

        self.reporte_strategy: ReporteStrategy = (
            ReporteStockStrategy()
        )

    def buscar_producto_por_sku(
        self,
        sku: str,
    ) -> Optional[Producto]:
        sku = str(sku).strip().upper()

        return next(
            (
                producto
                for producto in self.productos
                if producto.sku == sku
            ),
            None,
        )

    def buscar_licencia_por_codigo(
        self,
        codigo: str,
    ) -> Optional[LicenciaVirtual]:
        codigo = str(codigo).strip().upper()

        return next(
            (
                licencia
                for licencia in self.licencias
                if licencia.codigo_licencia == codigo
            ),
            None,
        )

    def buscar_licencias_por_sku(
        self,
        sku: str,
    ) -> List[LicenciaVirtual]:
        sku = str(sku).strip().upper()

        producto = self.buscar_producto_por_sku(
            sku
        )

        if producto is None:
            raise EntidadNoEncontradaError(
                f"No existe un producto con el SKU '{sku}'."
            )

        return [
            licencia
            for licencia in self.licencias
            if licencia.producto.sku == sku
        ]

    def buscar_cliente_por_documento(
        self,
        documento: str,
    ) -> Optional[Cliente]:
        documento = str(documento).strip()

        return next(
            (
                cliente
                for cliente in self.clientes
                if cliente.documento == documento
            ),
            None,
        )

    def registrar_producto(
        self,
        sku,
        nombre,
        duracion_meses,
        cantidad_equipos,
        costo_sin_igv_usd,
    ) -> Producto:
        if self.buscar_producto_por_sku(
            sku
        ) is not None:
            raise EntidadDuplicadaError(
                f"Ya existe un producto con el SKU '{sku}'."
            )

        producto = Producto(
            sku,
            nombre,
            duracion_meses,
            cantidad_equipos,
            costo_sin_igv_usd,
        )

        self.productos.append(
            producto
        )

        return producto

    def registrar_cliente(
        self,
        tipo,
        documento,
        nombre,
        correo,
        telefono,
        descuento,
    ) -> Cliente:
        if self.buscar_cliente_por_documento(
            documento
        ) is not None:
            raise EntidadDuplicadaError(
                f"Ya existe un cliente con el documento '{documento}'."
            )

        cliente = ClienteFactory.crear_cliente(
            tipo,
            documento,
            nombre,
            correo,
            telefono,
            descuento,
        )

        self.clientes.append(
            cliente
        )

        return cliente

    def registrar_licencia(
        self,
        codigo_licencia,
        sku_producto,
        fecha_ingreso,
    ) -> LicenciaVirtual:
        if self.buscar_licencia_por_codigo(
            codigo_licencia
        ) is not None:
            raise EntidadDuplicadaError(
                f"Ya existe una licencia con el código '{codigo_licencia}'."
            )

        producto = self.buscar_producto_por_sku(
            sku_producto
        )

        if producto is None:
            raise EntidadNoEncontradaError(
                f"No existe un producto con el SKU '{sku_producto}'."
            )

        licencia = LicenciaVirtual(
            codigo_licencia,
            producto,
            fecha_ingreso,
        )

        self.licencias.append(
            licencia
        )

        return licencia

    def vender_licencia(
        self,
        codigo_licencia,
        documento_cliente,
    ) -> LicenciaVirtual:
        licencia = self.buscar_licencia_por_codigo(
            codigo_licencia
        )

        if licencia is None:
            raise EntidadNoEncontradaError(
                f"No existe la licencia '{codigo_licencia}'."
            )

        cliente = self.buscar_cliente_por_documento(
            documento_cliente
        )

        if cliente is None:
            raise EntidadNoEncontradaError(
                f"No existe el cliente '{documento_cliente}'."
            )

        licencia.vender_a(
            cliente
        )

        return licencia

    def anular_licencia(
        self,
        codigo_licencia,
        motivo,
        con_devolucion,
    ) -> LicenciaVirtual:
        licencia = self.buscar_licencia_por_codigo(
            codigo_licencia
        )

        if licencia is None:
            raise EntidadNoEncontradaError(
                f"No existe la licencia '{codigo_licencia}'."
            )

        licencia.anular(
            motivo,
            con_devolucion,
        )

        return licencia

    def listar_licencias_por_estado(
        self,
        estado,
    ) -> List[LicenciaVirtual]:
        estado = validar_texto(
            estado,
            "estado",
        ).capitalize()

        if estado not in LicenciaVirtual.ESTADOS_VALIDOS:
            raise EstadoLicenciaError(
                "Estado no válido. Use Disponible, Vendida o Anulada."
            )

        return [
            licencia
            for licencia in self.licencias
            if licencia.estado == estado
        ]

    def configurar_reporte(
        self,
        strategy: ReporteStrategy,
    ) -> None:
        self.reporte_strategy = strategy

    def generar_reporte(self) -> str:
        return self.reporte_strategy.generar(
            self.licencias
        )
