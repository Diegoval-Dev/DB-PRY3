# database/client.py
"""
Módulo de conexión a MongoDB.

Expone la función `get_db()` que retorna una instancia única de la base de datos,
evitando múltiples conexiones con MongoClient.
"""

from pymongo import MongoClient
from configs.config import MONGO_URI, DB_NAME

_client = None

def get_db():
    """
    Devuelve la instancia de la base de datos especificada en DB_NAME.
    Utiliza un singleton para reutilizar la conexión de MongoClient.
    """
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client[DB_NAME]
