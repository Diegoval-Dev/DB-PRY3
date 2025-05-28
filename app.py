# app.py

import streamlit as st
from configs.config import LOG_LEVEL
from ui.create_puzzle import run as run_create_puzzle
from ui.map_piece import run as run_map_piece
from ui.display_instructions import run as run_display_instructions
import logging

def main():
    # Configurar logger
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=LOG_LEVEL
    )

    st.set_page_config(
        page_title="Puzzle Mapper",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar de navegación
    st.sidebar.title("Puzzle Mapper")
    page = st.sidebar.radio(
        "🗂️ Elige una sección:",
        ("1. Crear Puzzle", "2. Mapear Piezas", "3. Ver Instrucciones")
    )

    # Encabezado común
    st.markdown("## 🧩 Puzzle Mapper App")

    # Ruteo a la sección correspondiente
    if page.startswith("1"):
        run_create_puzzle()
    elif page.startswith("2"):
        run_map_piece()
    elif page.startswith("3"):
        run_display_instructions()
    else:
        st.error("Sección no válida")

if __name__ == "__main__":
    main()
