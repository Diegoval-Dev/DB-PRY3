"""
Configuración global del proyecto.

Carga las variables de entorno definidas en el archivo .env y valida
que las obligatorias estén presentes (MONGO_URI, DB_NAME).
También define el nivel de logging por defecto.
"""

import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Conexión a MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME   = os.getenv("DB_NAME")

# Nivel de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validaciones básicas
if not MONGO_URI:
    raise ValueError("La variable de entorno MONGO_URI no está definida.")
if not DB_NAME:
    raise ValueError("La variable de entorno DB_NAME no está definida.")
