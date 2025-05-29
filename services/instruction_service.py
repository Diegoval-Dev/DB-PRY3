# services/instruction_service.py
"""
Generación de instrucciones de armado de puzzles.

Requiere un puzzle y una pieza inicial para recorrer el grafo de vecinos
y generar pasos secuenciales de ensamblaje.
"""
from typing import List, Set
from services.puzzle_service import list_pieces
from models.piece import Piece

def generate_instructions(puzzle_id: str, start_code: str) -> List[str]:
    """
    Genera instrucciones atómicas para armar el puzzle:
    1) Explica cómo numerar las uniones de la pieza base.
    2) Recorre el grafo de vecinos y emite 'Une la pieza X a la Conexión k de Y.'
    """

    pieces = list_pieces(puzzle_id)
    code_map = {p.code: p for p in pieces}

    if start_code not in code_map:
        raise ValueError(f"Pieza de inicio '{start_code}' no encontrada en el puzzle.")

    instructions: List[str] = []
    visited: Set[str] = set()

    # Instrucción inicial sin numerar
    instructions.append(
        "Coloca la pieza **{0}** sobre la mesa con la etiqueta en la parte superior, orientada hacia el norte.".format(start_code)
    )
    instructions.append(
        "Imagina que recorres el contorno de la pieza en el sentido de las agujas del reloj; numera cada punto de unión que encuentres: "
        "la primera será **Conexión 1**, la siguiente **Conexión 2**, y así sucesivamente."
    )

    def dfs(current_code: str):
        visited.add(current_code)
        current_piece: Piece = code_map[current_code]

        for nb in current_piece.neighbors:
            k = nb.edgeId
            neighbor = nb.neighborCode
            if not neighbor or neighbor in visited:
                continue

            instructions.append(
                "Une la pieza **{0}** a la Conexión **{1}** de **{2}**. "
                "Para ello, coloca {0} junto a {2}, orientando su propia Conexión {1} de modo que encaje perfectamente.".format(
                    neighbor, k, current_code
                )
            )
            dfs(neighbor)

    dfs(start_code)
    return instructions
