class ErrorSistemaLicencias(Exception):
    """Excepción base del sistema."""

class CampoVacioError(ErrorSistemaLicencias):
    pass

class DatoInvalidoError(ErrorSistemaLicencias):
    pass

class EntidadDuplicadaError(ErrorSistemaLicencias):
    pass

class EntidadNoEncontradaError(ErrorSistemaLicencias):
    pass

class EstadoLicenciaError(ErrorSistemaLicencias):
    pass
