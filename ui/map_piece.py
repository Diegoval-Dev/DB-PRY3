# ui/map_piece.py

import streamlit as st
from services.puzzle_service import list_puzzles, add_piece, list_pieces
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

    # 2. Listado de piezas ya mapeadas
    st.subheader("📋 Piezas mapeadas")
    existing: list[Piece] = list_pieces(puzzle.id)
    if existing:
        for p in existing:
            st.write(f"- Código: **{p.code}**, Sector: **{p.sector}**")
    else:
        st.info("Aún no has mapeado ninguna pieza para este puzzle.")

    st.markdown("---")
    st.subheader("📝 Mapear nueva pieza")

    # 3. Formulario de mapeo
    with st.form("map_piece_form", clear_on_submit=True):
        code = st.text_input("Código de la pieza", help="Ejemplo: P1")
        sector = st.selectbox("Sector", puzzle.sectors)

        # Para cada uno de los 4 bordes
        edge_types: dict[int,str] = {}
        edge_neighbors: dict[int, str] = {}
        neighbor_options = ["NINGUNO"] + [p.code for p in existing]

        for edge_id in (1, 2, 3, 4):
            st.markdown(f"**Borde {edge_id}**")
            edge_types[edge_id] = st.selectbox(
                f"Tipo en borde {edge_id}",
                ("hembra", "macho"),
                key=f"type_{edge_id}"
            )
            edge_neighbors[edge_id] = st.selectbox(
                f"Vecino en borde {edge_id}",
                neighbor_options,
                key=f"neighbor_{edge_id}"
            )

        submitted = st.form_submit_button("➕ Guardar Pieza")

    # 4. Procesar envío
    if submitted:
        if not code:
            st.error("❌ Debes indicar el código de la pieza.")
        else:
            # Construir estructuras para add_piece
            edges = [
                {"edgeId": eid, "type": edge_types[eid]}
                for eid in (1, 2, 3, 4)
            ]
            neighbors = []
            for eid in (1, 2, 3, 4):
                nb = edge_neighbors[eid]
                neighbors.append({
                    "edgeId": eid,
                    "neighborPiece": nb if nb != "NINGUNO" else None
                })

            try:
                piece: Piece = add_piece(puzzle.id, code, sector, edges, neighbors)
                st.success(f"✔️ Pieza **{piece.code}** guardada correctamente.")
            except Exception as e:
                st.error(f"Error al guardar la pieza: {e}")

            # Refrescar listado de piezas
            existing = list_pieces(puzzle.id)
