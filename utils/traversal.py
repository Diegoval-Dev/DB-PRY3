# utils/traversal.py

from typing import Dict, List, Set, Optional
from models.piece import Piece

# Mapeo de edgeId a nombre de dirección (reutilizado por instruction_service)
EDGE_DIRECTION = {
    1: "norte",
    2: "este",
    3: "sur",
    4: "oeste"
}

def dfs_traverse(
    pieces: List[Piece],
    start_code: str,
    on_visit: Optional[callable] = None
) -> None:
    """
    Recorrido en profundidad (DFS) sobre el grafo de piezas.
    - pieces: lista de Piece con 'code' y 'neighbors'
    - start_code: código de la pieza inicial
    - on_visit: función opcional que recibe (current: Piece, neighbor: Piece, edgeId: int)
      por cada arista recorrida; útil para generar instrucciones.
    """
    code_map: Dict[str, Piece] = {p.code: p for p in pieces}
    id_map:   Dict[str, str]   = {p.id:   p.code for p in pieces}
    visited: Set[str] = set()

    def _dfs(current_code: str):
        visited.add(current_code)
        current_piece = code_map[current_code]

        for nb in current_piece.neighbors:
            if not nb.neighborPiece:
                continue
            neighbor_code = id_map.get(nb.neighborPiece)
            if not neighbor_code or neighbor_code in visited:
                continue

            if on_visit:
                on_visit(current_piece, code_map[neighbor_code], nb.edgeId)

            _dfs(neighbor_code)

    if start_code not in code_map:
        raise ValueError(f"Pieza inicial '{start_code}' no encontrada.")
    _dfs(start_code)
