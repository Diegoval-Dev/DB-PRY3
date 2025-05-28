# services/instruction_service.py

from typing import List, Dict, Set
from services.puzzle_service import get_piece, list_pieces
from models.piece import Piece

# Mapeo de edgeId a nombre de dirección
EDGE_DIRECTION: Dict[int, str] = {
    1: "norte",
    2: "este",
    3: "sur",
    4: "oeste"
}

def generate_instructions(puzzle_id: str, start_code: str) -> List[str]:
    """
    Genera instrucciones atómicas para armar el puzzle,
    recorriendo las piezas desde start_code en profundidad (DFS).
    """
    # Obtiene todas las piezas y construye mapas auxiliares
    pieces: List[Piece] = list_pieces(puzzle_id)
    code_map: Dict[str, Piece] = {p.code: p for p in pieces}
    id_map:   Dict[str, str]   = {p.id:   p.code for p in pieces}

    if start_code not in code_map:
        raise ValueError(f"Pieza de inicio '{start_code}' no encontrada en el puzzle.")

    visited: Set[str] = set()
    instructions: List[str] = []

    def dfs(current_code: str):
        visited.add(current_code)
        current_piece = code_map[current_code]

        for neighbor in current_piece.neighbors:
            edge = neighbor.edgeId
            neighbor_id = neighbor.neighborPiece

            # Si no hay pieza (hueco), lo omitimos
            if not neighbor_id:
                continue

            # Traducir ObjectId (str) a código legible
            neighbor_code = id_map.get(neighbor_id)
            if not neighbor_code or neighbor_code in visited:
                continue

            direction = EDGE_DIRECTION.get(edge, f"borde {edge}")
            # Instrucción atómica
            instructions.append(
                f"Une la pieza {neighbor_code} al {direction} de {current_code}."
            )
            # Recursión
            dfs(neighbor_code)

    # Paso 1: colocar pieza base
    instructions.append(f"Coloca la pieza {start_code} como base.")
    dfs(start_code)

    return instructions
