# utils/logger.py
"""
Configuración del sistema de logging.

Permite obtener loggers personalizados con formato estandarizado
usando el nivel definido en las variables de entorno.
"""

import logging
from configs.config import LOG_LEVEL

# Convertir nivel de logging de texto a constante de logging
_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)

# Configuración básica – se puede importar desde cualquier módulo
logging.basicConfig(
    level=_level,
    format="%(asctime)s %(levelname)s [%(name)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name: str) -> logging.Logger:
    """
    Devuelve un logger nombrado, con la configuración global aplicada.
    """
    return logging.getLogger(name)
