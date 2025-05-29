# services/puzzle_service.py
"""
Servicios relacionados con los puzzles y piezas.

Funciones de alto nivel que gestionan los datos del puzzle,
abstrayendo la lógica de acceso a la base de datos.
"""
from typing import List, Optional, Dict, Any
from bson import ObjectId
from datetime import datetime

from database.repositories import (
    create_puzzle       as repo_create_puzzle,
    get_puzzle_by_id    as repo_get_puzzle,
    get_all_puzzles     as repo_list_puzzles,
    update_puzzle       as repo_update_puzzle,
    delete_puzzle       as repo_delete_puzzle,
    create_piece        as repo_create_piece,
    get_piece_by_code   as repo_get_piece_by_code,
    get_pieces_by_puzzle as repo_list_pieces,
    update_piece        as repo_update_piece,
)
from models.puzzle import Puzzle
from models.piece import Piece

# ─── P U Z Z L E S ────────────────────────────────────────────────────────────

def add_puzzle(
    name: str, totalPieces: int, sectors: List[str]
) -> Puzzle:
    """Crea un nuevo puzzle y lo devuelve como modelo."""
    doc = {
        "name": name,
        "totalPieces": totalPieces,
        "sectors": sectors,
        "createdAt": datetime.now()  # Usamos la fecha actual
    }
    created = repo_create_puzzle(doc)
    return Puzzle(**created)

def get_puzzle(puzzle_id: str) -> Optional[Puzzle]:
    """Recupera un puzzle por su ID."""
    raw = repo_get_puzzle(puzzle_id)
    return Puzzle(**raw) if raw else None

def list_puzzles() -> List[Puzzle]:
    """Lista todos los puzzles."""
    raws = repo_list_puzzles()
    return [Puzzle(**_prepare_document(r)) for r in raws]

def update_puzzle_info(puzzle_id: str, update_data: dict) -> Optional[Puzzle]:
    """Actualiza campos de un puzzle."""
    updated = repo_update_puzzle(puzzle_id, update_data)
    return Puzzle(**_prepare_document(updated)) if updated else None

def remove_puzzle(puzzle_id: str) -> bool:
    """Elimina un puzzle."""
    return repo_delete_puzzle(puzzle_id)

# ─── P I E C E S ───────────────────────────────────────────────────────────────

def add_or_update_piece(
    puzzle_id: str,
    code: str,
    sector: str,
    edges: list[dict],
    neighbors: list[dict]
) -> Piece:
    """
    Si la pieza (puzzleId+code) existe, la actualiza con los nuevos fields.
    Si no existe, la crea.
    """
    # 1) Preparamos el documento _parcial_ de actualización/creación
    doc = {
        "puzzleId": ObjectId(puzzle_id),
        "code": code,
        "sector": sector,
        "edges": edges,
        "neighbors": neighbors
    }

    # 2) ¿Ya existe esa pieza?
    existing = repo_get_piece_by_code(puzzle_id, code)
    if existing:
        # update_piece espera id como str y un dict con los campos a settear
        updated = repo_update_piece(str(existing["_id"]), {
            "sector": sector,
            "edges": edges,
            "neighbors": neighbors
        })
        return Piece(**updated)

    # 3) No existe → la creamos
    created = repo_create_piece(doc)
    return Piece(**created)

def get_piece(
    puzzle_id: str,
    code: str
) -> Optional[Piece]:
    """Recupera una pieza por su código dentro de un puzzle."""
    raw = repo_get_piece_by_code(puzzle_id, code)
    return Piece(**_prepare_document(raw)) if raw else None

def list_pieces(puzzle_id: str) -> List[Piece]:
    """Lista todas las piezas de un puzzle."""
    raws = repo_list_pieces(puzzle_id)
    return [Piece(**_prepare_document(r)) for r in raws]

def update_piece_info(
    piece_id: str,
    update_data: dict
) -> Optional[Piece]:
    """Actualiza campos de una pieza."""
    updated = repo_update_piece(piece_id, update_data)
    return Piece(**_prepare_document(updated)) if updated else None

# ─── U T I L I T I E S ────────────────────────────────────────────────────────

def _prepare_document(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepara un documento de MongoDB para ser convertido a un modelo Pydantic.
    - Convierte ObjectId a string
    - Asegura que valores como createdAt tengan valores válidos
    """
    if not doc:
        return {}
    
    result = dict(doc)
    
    # Convertir _id de ObjectId a string
    if '_id' in result and isinstance(result['_id'], ObjectId):
        result['_id'] = str(result['_id'])
    
    # Convertir puzzleId de ObjectId a string si existe
    if 'puzzleId' in result and isinstance(result['puzzleId'], ObjectId):
        result['puzzleId'] = str(result['puzzleId'])
    
    # Asegurar que createdAt tenga un valor válido
    if 'createdAt' in result and result['createdAt'] is None:
        result['createdAt'] = datetime.now()
    
    # Procesar neighbors si existen
    if 'neighbors' in result and result['neighbors']:
        for neighbor in result['neighbors']:
            if 'neighborPiece' in neighbor and isinstance(neighbor['neighborPiece'], ObjectId):
                neighbor['neighborPiece'] = str(neighbor['neighborPiece'])
    
    return result
