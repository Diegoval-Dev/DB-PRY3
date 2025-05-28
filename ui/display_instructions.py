# ui/display_instructions.py

import streamlit as st
from services.puzzle_service import list_puzzles, list_pieces
from services.instruction_service import generate_instructions
from models.puzzle import Puzzle
from models.piece import Piece

def run():
    st.header("3️⃣ Ver instrucciones de armado")

    # 1. Selección de Puzzle
    puzzles = list_puzzles()
    if not puzzles:
        st.info("No hay puzzles creados. Crea uno primero en la sección ‘Crear Puzzle’.")
        return

    puzzle: Puzzle = st.selectbox(
        "Selecciona un puzzle",
        puzzles,
        format_func=lambda p: f"{p.name} (ID: {p.id})"
    )

    # 2. Obtener lista de códigos de piezas mapeadas
    pieces: list[Piece] = list_pieces(puzzle.id)
    if not pieces:
        st.info("Aún no hay piezas mapeadas en este puzzle. Ve a ‘Mapear Piezas’ primero.")
        return

    codes = [p.code for p in pieces]
    start_code = st.selectbox("Seleccione la pieza base", codes)

    # 3. Generar instrucciones
    if st.button("🧩 Generar instrucciones"):
        try:
            instructions = generate_instructions(puzzle.id, start_code)
            st.subheader("Pasos para armar tu rompecabezas:")
            for i, inst in enumerate(instructions, start=1):
                st.write(f"{i}. {inst}")
        except Exception as e:
            st.error(f"Error al generar instrucciones: {e}")
