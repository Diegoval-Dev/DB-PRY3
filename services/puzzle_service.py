# services/puzzle_service.py

from typing import List, Optional
from bson import ObjectId

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
        "createdAt": None  # MongoDB asigna la fecha automáticamente si lo configuras, o bien lo puedes llenar aquí
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
    return [Puzzle(**r) for r in raws]

def update_puzzle_info(puzzle_id: str, update_data: dict) -> Optional[Puzzle]:
    """Actualiza campos de un puzzle."""
    updated = repo_update_puzzle(puzzle_id, update_data)
    return Puzzle(**updated) if updated else None

def remove_puzzle(puzzle_id: str) -> bool:
    """Elimina un puzzle."""
    return repo_delete_puzzle(puzzle_id)

# ─── P I E C E S ───────────────────────────────────────────────────────────────

def add_piece(
    puzzle_id: str,
    code: str,
    sector: str,
    edges: List[dict],
    neighbors: List[dict]
) -> Piece:
    """Crea una pieza dentro de un puzzle."""
    # Asegurar que el puzzle existe
    if not repo_get_puzzle(puzzle_id):
        raise ValueError(f"Puzzle {puzzle_id} no encontrado.")
    doc = {
        "puzzleId": ObjectId(puzzle_id),
        "code": code,
        "sector": sector,
        "edges": edges,
        "neighbors": [
            {
                "edgeId": nb["edgeId"],
                "neighborPiece": ObjectId(nb["neighborPiece"]) if nb["neighborPiece"] else None
            }
            for nb in neighbors
        ]
    }
    created = repo_create_piece(doc)
    return Piece(**created)

def get_piece(
    puzzle_id: str,
    code: str
) -> Optional[Piece]:
    """Recupera una pieza por su código dentro de un puzzle."""
    raw = repo_get_piece_by_code(puzzle_id, code)
    return Piece(**raw) if raw else None

def list_pieces(puzzle_id: str) -> List[Piece]:
    """Lista todas las piezas de un puzzle."""
    raws = repo_list_pieces(puzzle_id)
    return [Piece(**r) for r in raws]

def update_piece_info(
    piece_id: str,
    update_data: dict
) -> Optional[Piece]:
    """Actualiza campos de una pieza."""
    updated = repo_update_piece(piece_id, update_data)
    return Piece(**updated) if updated else None
