from .cliente import CanalVenta, Cliente, Mayorista
from .excepciones import DatoInvalidoError

class ClienteFactory:
    @staticmethod
    def crear_cliente(
        tipo,
        documento,
        nombre,
        correo,
        telefono,
        descuento,
    ) -> Cliente:
        tipo_normalizado = str(tipo).strip().lower()

        if tipo_normalizado in {"1", "mayorista"}:
            return Mayorista(
                documento,
                nombre,
                correo,
                telefono,
                descuento,
            )

        if tipo_normalizado in {
            "2",
            "canal",
            "canal de venta",
        }:
            return CanalVenta(
                documento,
                nombre,
                correo,
                telefono,
                descuento,
            )

        raise DatoInvalidoError(
            "Tipo de cliente no válido."
        )
