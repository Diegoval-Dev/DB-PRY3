# services/instruction_service.py
"""
Generación de instrucciones de armado de puzzles.

Requiere un puzzle y una pieza inicial para recorrer el grafo de vecinos
y generar pasos secuenciales de ensamblaje.
"""
from typing import List, Set
from services.puzzle_service import list_pieces
from models.piece import Piece
from utils.logger import get_logger

# Crear logger para este módulo
logger = get_logger(__name__)

def generate_instructions(puzzle_id: str, start_code: str) -> List[str]:
    """
    Genera instrucciones atómicas para armar el puzzle:
    1) Explica cómo numerar las uniones de la pieza base.
    2) Recorre el grafo de vecinos y emite 'Une la pieza X a la Conexión k de Y.'
    
    Ahora es resistente a piezas faltantes:
    - Si la pieza inicial no existe, muestra un error claro
    - Si hay piezas vecinas faltantes, las omite y continúa
    - Informa sobre las piezas faltantes en las instrucciones
    """

    pieces = list_pieces(puzzle_id)
    code_map = {p.code: p for p in pieces}
    
    # Lista para rastrear piezas faltantes
    missing_pieces: Set[str] = set()

    if start_code not in code_map:
        logger.warning(f"Pieza inicial '{start_code}' no encontrada en el puzzle {puzzle_id}")
        return [f"⚠️ Error: La pieza inicial **{start_code}** no se encuentra en la base de datos. "
                f"Por favor, verifica que existe y vuelve a intentarlo."]

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
            
            # Omitir si no hay vecino definido o ya fue visitado
            if not neighbor or neighbor in visited:
                continue
            
            # Verificar si el vecino existe en el código
            if neighbor not in code_map:
                missing_pieces.add(neighbor)
                instructions.append(
                    f"⚠️ **Nota**: La pieza **{neighbor}** que debería conectarse a la Conexión **{k}** de **{current_code}** "
                    f"no se encuentra en la base de datos. Continúa con las siguientes piezas disponibles."
                )
                continue

            instructions.append(
                "Une la pieza **{0}** a la Conexión **{1}** de **{2}**. "
                "Para ello, busca en la pieza {0} el punto de unión que encaje con la Conexión {1} de {2} y conéctalos de modo que encajen perfectamente.".format(
                    neighbor, k, current_code
                )
            )
            dfs(neighbor)

    dfs(start_code)
    
    # Agregar resumen de piezas faltantes al final si hay alguna
    if missing_pieces:
        instructions.append("\n⚠️ **Resumen de piezas faltantes**: " + 
                           ", ".join([f"**{p}**" for p in sorted(missing_pieces)]) +
                           ". Estas piezas están referenciadas en el mapa pero no se encuentran en la base de datos.")
    
    return instructions
