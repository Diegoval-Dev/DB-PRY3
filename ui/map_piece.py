# ui/map_piece.py
"""
Interfaz Streamlit para mapear piezas a un puzzle existente.

Incluye selección del puzzle, definición de conexiones (edges) y vecinos (neighbors).
"""

import streamlit as st
from services.puzzle_service import list_puzzles, add_or_update_piece as add_piece, list_pieces
from models.puzzle import Puzzle
from models.piece import Piece

def run():
    st.header("2️⃣ Mapear piezas del Puzzle")

    # 1. Selección de Puzzle
    puzzles = list_puzzles()
    if not puzzles:
        st.info("No hay puzzles creados. Por favor, crea uno primero en la sección ‘Crear Puzzle’.")
        return

    puzzle: Puzzle = st.selectbox(
        "Selecciona un Puzzle",
        puzzles,
        format_func=lambda p: f"{p.name} (ID: {p.id})"
    )

    # Función para obtener y mostrar piezas existentes
    def refresh_existing():
        pieces = list_pieces(puzzle.id)
        if pieces:
            st.subheader("📋 Piezas mapeadas")
            for p in pieces:
                st.write(f"- Código: **{p.code}**, Sector: **{p.sector}**")
        else:
            st.info("Aún no has mapeado ninguna pieza para este puzzle.")
        return pieces

    existing: list[Piece] = refresh_existing()

    st.markdown("---")
    st.subheader("📝 Mapear nueva pieza")
    
    # Inicializar edge_count una sola vez
    st.session_state.setdefault("edge_count", 1)

    # 2. Formulario de mapeo
    with st.form("map_piece_form", clear_on_submit=False):
        code = st.text_input("Código de la pieza", help="Ejemplo: P1")
        sector = st.selectbox("Sector", puzzle.sectors)

        # number_input con key para persistencia automática
        edge_count = st.number_input(
            "Número de conexiones",
            min_value=1, max_value=6,
            value=st.session_state.edge_count,
            key="edge_count"
        )

        edge_types: dict[int, str] = {}
        edge_neighbors: dict[int, str] = {}

        for eid in range(1, edge_count + 1):
            st.markdown(f"**Conexión {eid}**")
            edge_types[eid] = st.selectbox(
                f"Tipo de conexión {eid}",
                ("hembra", "macho"),
                key=f"type_{eid}"
            )
            edge_neighbors[eid] = st.text_input(
                f"Código de la pieza vecina para conexión {eid} (opcional)",
                key=f"neighbor_{eid}"
            )

        # Submit button dentro del form
        submitted = st.form_submit_button("➕ Guardar Pieza")

    # 3. Procesar envío y refetch
    if submitted:
        if not code:
            st.error("❌ Debes indicar el código de la pieza.")
            return

        # Construir edges y neighbors usando el edge_count actual
        edges = [
            {"edgeId": eid, "type": edge_types[eid]}
            for eid in range(1, edge_count + 1)
        ]
        neighbors = [
            {
                "edgeId": eid,
                "neighborCode": (edge_neighbors[eid].strip() or None)
            }
            for eid in range(1, edge_count + 1)
        ]

        try:
            piece: Piece = add_piece(puzzle.id, code, sector, edges, neighbors)
            st.success(f"✔️ Pieza **{piece.code}** guardada correctamente.")
        except Exception as e:
            st.error(f"Error al guardar la pieza: {e}")

        # Refrescar lista y reiniciar la app
        refresh_existing()
        st.experimental_rerun()
