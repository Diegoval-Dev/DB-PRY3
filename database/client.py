# database/client.py

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
