# database/repositories.py

from typing import List, Optional
from bson import ObjectId
from database.client import get_db

# Obtener las colecciones
db = get_db()
_puzzles = db.puzzles
_pieces  = db.pieces

# ─── P U Z Z L E S ────────────────────────────────────────────────────────────

def create_puzzle(puzzle_doc: dict) -> dict:
    """
    Inserta un nuevo puzzle y devuelve el documento creado (con _id).
    """
    result = _puzzles.insert_one(puzzle_doc)
    return _puzzles.find_one({"_id": result.inserted_id})

def get_puzzle_by_id(puzzle_id: str) -> Optional[dict]:
    """
    Obtiene un puzzle por su _id (string).
    """
    return _puzzles.find_one({"_id": ObjectId(puzzle_id)})

def get_all_puzzles() -> List[dict]:
    """
    Devuelve todos los puzzles.
    """
    return list(_puzzles.find())

def update_puzzle(puzzle_id: str, update_doc: dict) -> Optional[dict]:
    """
    Actualiza campos de un puzzle y devuelve el puzzle actualizado.
    """
    _puzzles.update_one(
        {"_id": ObjectId(puzzle_id)},
        {"$set": update_doc}
    )
    return get_puzzle_by_id(puzzle_id)

def delete_puzzle(puzzle_id: str) -> bool:
    """
    Elimina un puzzle. Devuelve True si se borró al menos un documento.
    """
    result = _puzzles.delete_one({"_id": ObjectId(puzzle_id)})
    return result.deleted_count > 0

# ─── P I E C E S ───────────────────────────────────────────────────────────────

def create_piece(piece_doc: dict) -> dict:
    """
    Inserta una nueva pieza y devuelve el documento creado (con _id).
    """
    result = _pieces.insert_one(piece_doc)
    return _pieces.find_one({"_id": result.inserted_id})

def get_piece_by_id(piece_id: str) -> Optional[dict]:
    """
    Obtiene una pieza por su _id (string).
    """
    return _pieces.find_one({"_id": ObjectId(piece_id)})

def get_piece_by_code(puzzle_id: str, code: str) -> Optional[dict]:
    """
    Busca una pieza dentro de un puzzle por su código legible (P1, P2…).
    """
    return _pieces.find_one({
        "puzzleId": ObjectId(puzzle_id),
        "code": code
    })

def get_pieces_by_puzzle(puzzle_id: str) -> List[dict]:
    """
    Devuelve todas las piezas de un puzzle.
    """
    return list(_pieces.find({"puzzleId": ObjectId(puzzle_id)}))

def update_piece(piece_id: str, update_doc: dict) -> Optional[dict]:
    """
    Actualiza campos de una pieza y devuelve la pieza actualizada.
    """
    _pieces.update_one(
        {"_id": ObjectId(piece_id)},
        {"$set": update_doc}
    )
    return get_piece_by_id(piece_id)

def delete_piece(piece_id: str) -> bool:
    """
    Elimina una pieza. Devuelve True si se borró al menos un documento.
    """
    result = _pieces.delete_one({"_id": ObjectId(piece_id)})
    return result.deleted_count > 0
