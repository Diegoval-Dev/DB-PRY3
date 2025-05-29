# ui/create_puzzle.py
"""
Interfaz Streamlit para la creación de nuevos puzzles.

Permite ingresar el nombre, número total de piezas y sectores.
Lista puzzles ya existentes.
"""
import streamlit as st
from services.puzzle_service import add_puzzle, list_puzzles
from models.puzzle import Puzzle

def run():
    st.header("1️⃣ Crear nuevo Puzzle")

    # Formulario de creación
    with st.form("create_puzzle_form", clear_on_submit=True):
        name = st.text_input("Nombre del rompecabezas", help="Ejemplo: Caracol Espiral")
        total_pieces = st.number_input(
            "Número estimado de piezas",
            min_value=1,
            step=1,
            help="Cantidad total de piezas (contadas o aproximadas)"
        )
        sectors_input = st.text_input(
            "Sectores (separados por comas)",
            help="Define zonas lógicas, por ejemplo: A,B,C,D"
        )

        submitted = st.form_submit_button("➕ Crear Puzzle")

    if submitted:
        # Validación básica
        if not name:
            st.error("❌ Debes indicar un nombre para el puzzle.")
        elif not sectors_input.strip():
            st.error("❌ Debes definir al menos un sector.")
        else:
            sectors = [s.strip() for s in sectors_input.split(",") if s.strip()]
            try:
                puzzle: Puzzle = add_puzzle(name, total_pieces, sectors)
                st.success(f"✔️ Puzzle creado: **{puzzle.name}** (ID: `{puzzle.id}`)")
            except Exception as e:
                st.error(f"Error al crear el puzzle: {e}")

    # Listado de puzzles existentes
    st.markdown("---")
    st.subheader("📋 Puzzles existentes")
    puzzles = list_puzzles()
    if puzzles:
        for p in puzzles:
            st.write(f"- **{p.name}**  (ID: `{p.id}`, piezas: {p.totalPieces}, sectores: {p.sectors})")
    else:
        st.info("Aún no hay puzzles registrados.")
