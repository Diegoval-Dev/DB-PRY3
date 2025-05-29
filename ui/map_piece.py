# ui/map_piece.py
"""
Interfaz Streamlit para mapear piezas a un puzzle existente.

Incluye selección del puzzle, definición de conexiones (edges) y vecinos (neighbors)
usando direcciones cardinales para mejor intuición espacial.
"""

import streamlit as st
from services.puzzle_service import list_puzzles, add_or_update_piece as add_piece, list_pieces, get_piece
from models.puzzle import Puzzle
from models.piece import Piece, Edge, Neighbor

# Mapeo de dirección a edgeId para mantener compatibilidad con el modelo existente
DIRECTION_TO_EDGE = {
    "Norte": 1,
    "Este": 2,
    "Sur": 3,
    "Oeste": 4,
    "Arriba": 5,  # Para puzzles 3D o con capas
    "Abajo": 6    # Para puzzles 3D o con capas
}

# Mapeo inverso para mostrar
EDGE_TO_DIRECTION = {v: k for k, v in DIRECTION_TO_EDGE.items()}

# Direcciones opuestas para conexiones bidireccionales
OPPOSITE_DIRECTION = {
    "Norte": "Sur",
    "Este": "Oeste",
    "Sur": "Norte",
    "Oeste": "Este",
    "Arriba": "Abajo",
    "Abajo": "Arriba"
}

def run():
    st.header("2️⃣ Mapear piezas del Puzzle")

    # 1. Selección de Puzzle
    puzzles = list_puzzles()
    if not puzzles:
        st.info("No hay puzzles creados. Por favor, crea uno primero en la sección 'Crear Puzzle'.")
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
            
            # Organizar en columnas para mejor visualización
            cols = st.columns(3)
            for i, p in enumerate(pieces):
                with cols[i % 3]:
                    with st.expander(f"**{p.code}** ({p.sector})"):
                        for edge in p.edges:
                            direction = EDGE_TO_DIRECTION.get(edge.edgeId, f"Conexión {edge.edgeId}")
                            neighbor_code = next((n.neighborCode for n in p.neighbors if n.edgeId == edge.edgeId), None)
                            if neighbor_code:
                                st.write(f"- {direction}: {edge.type} → conecta con **{neighbor_code}**")
                            else:
                                st.write(f"- {direction}: {edge.type}")
                        
                        # Opción para editar la pieza
                        if st.button(f"✏️ Editar {p.code}", key=f"edit_{p.code}"):
                            st.session_state.editing_piece = p.code
        else:
            st.info("Aún no has mapeado ninguna pieza para este puzzle.")
        return pieces

    existing: list[Piece] = refresh_existing()

    # Verificar si estamos editando una pieza
    editing_piece_code = st.session_state.get("editing_piece", None)
    editing_piece = None
    
    if editing_piece_code:
        editing_piece = next((p for p in existing if p.code == editing_piece_code), None)
        if editing_piece:
            st.success(f"Editando pieza: **{editing_piece_code}**")
    
    st.markdown("---")
    
    # Guía visual para el usuario
    with st.expander("ℹ️ Guía de orientación para mapear piezas", expanded=not bool(existing)):
        st.markdown("""
        ### Cómo orientar tus piezas
        
        Para cada pieza de tu rompecabezas:
        
        1. **Orientación**: Sostén la pieza frente a ti con la parte superior hacia arriba.
        2. **Direcciones**: 
           - **Norte** ⬆️: Borde superior
           - **Este** ➡️: Borde derecho
           - **Sur** ⬇️: Borde inferior
           - **Oeste** ⬅️: Borde izquierdo
           
        3. **Tipos de conexión**:
           - **Macho**: Borde que sobresale (tab)
           - **Hembra**: Borde con hueco (slot)
           
        4. **Conexiones**: Para cada dirección, indica:
           - Tipo de borde (macho/hembra)
           - Código de la pieza que conecta (si ya la conoces)
           
        <div style='text-align: center'>
            <pre>
              Norte
                ⬆️
        Oeste ⬅️   ➡️ Este
                ⬇️
               Sur
            </pre>
        </div>
        """)
    
    st.subheader("📝 " + ("Editar" if editing_piece else "Mapear nueva") + " pieza")
    
    # Determinar direcciones disponibles
    available_directions = list(DIRECTION_TO_EDGE.keys())[:4]  # Por defecto solo N, E, S, W
    if "use_3d" in st.session_state and st.session_state.use_3d:
        available_directions = list(DIRECTION_TO_EDGE.keys())  # Incluir Arriba/Abajo
    
    # Checkbox para habilitar 3D (Arriba/Abajo)
    use_3d = st.checkbox("Habilitar conexiones 3D (Arriba/Abajo)", 
                          value=st.session_state.get("use_3d", False),
                          key="use_3d")
    
    # 2. Formulario de mapeo
    with st.form("map_piece_form", clear_on_submit=False):
        # Si estamos editando, pre-rellenar campos
        default_code = editing_piece.code if editing_piece else ""
        default_sector = editing_piece.sector if editing_piece else puzzle.sectors[0]
        
        code = st.text_input("Código de la pieza", 
                             value=default_code,
                             help="Ejemplo: P1, A3, etc.")
        
        sector = st.selectbox("Sector", 
                              puzzle.sectors,
                              index=puzzle.sectors.index(default_sector) if editing_piece else 0)
        
        # Mostrar visualización simple de la pieza
        st.markdown("### Conexiones de la pieza")
        st.markdown("Selecciona las direcciones que tienen conexiones y su tipo:")
        
        edge_types = {}
        edge_neighbors = {}
        
        # Para cada dirección, mostrar opciones de conexión
        cols = st.columns(len(available_directions))
        for i, direction in enumerate(available_directions):
            with cols[i]:
                st.markdown(f"**{direction}**")
                
                # Determinar valores por defecto si estamos editando
                has_edge = False
                default_type = "hembra"
                default_neighbor = ""
                
                if editing_piece:
                    edge_id = DIRECTION_TO_EDGE[direction]
                    edge = next((e for e in editing_piece.edges if e.edgeId == edge_id), None)
                    if edge:
                        has_edge = True
                        default_type = edge.type
                        neighbor = next((n for n in editing_piece.neighbors if n.edgeId == edge_id), None)
                        if neighbor and neighbor.neighborCode:
                            default_neighbor = neighbor.neighborCode
                
                # Checkbox para habilitar/deshabilitar esta conexión
                has_connection = st.checkbox(
                    f"Tiene conexión", 
                    value=has_edge,
                    key=f"has_{direction}"
                )
                
                if has_connection:
                    edge_types[direction] = st.selectbox(
                        f"Tipo",
                        ("hembra", "macho"),
                        index=0 if default_type == "hembra" else 1,
                        key=f"type_{direction}"
                    )
                    
                    # Lista de piezas existentes para seleccionar
                    existing_codes = [p.code for p in existing if p.code != code]
                    if default_neighbor and default_neighbor not in existing_codes:
                        existing_codes = [default_neighbor] + existing_codes
                    
                    # Primero mostramos selector de pieza existente
                    use_existing = st.checkbox(
                        "Conectar con pieza existente", 
                        value=bool(default_neighbor and default_neighbor in existing_codes),
                        key=f"use_existing_{direction}"
                    )
                    
                    if use_existing and existing_codes:
                        neighbor_idx = 0
                        if default_neighbor in existing_codes:
                            neighbor_idx = existing_codes.index(default_neighbor)
                            
                        selected_neighbor = st.selectbox(
                            "Pieza vecina",
                            existing_codes,
                            index=neighbor_idx,
                            key=f"select_neighbor_{direction}"
                        )
                        edge_neighbors[direction] = selected_neighbor
                    else:
                        # O permitimos texto libre para piezas que se crearán después
                        edge_neighbors[direction] = st.text_input(
                            "Código de pieza vecina",
                            value=default_neighbor,
                            help="Déjalo en blanco si no conoces la pieza vecina aún",
                            key=f"neighbor_{direction}"
                        )

        # Submit button dentro del form
        submit_label = "✏️ Actualizar Pieza" if editing_piece else "➕ Guardar Pieza"
        submitted = st.form_submit_button(submit_label)
        
        # Botón para cancelar edición
        if editing_piece and st.form_submit_button("❌ Cancelar Edición"):
            st.session_state.pop("editing_piece", None)
            st.rerun()

    # 3. Procesar envío y refetch
    if submitted:
        if not code:
            st.error("❌ Debes indicar el código de la pieza.")
            return

        # Construir edges y neighbors usando las direcciones seleccionadas
        edges = []
        neighbors = []
        
        for direction in available_directions:
            if st.session_state.get(f"has_{direction}", False):
                edge_id = DIRECTION_TO_EDGE[direction]
                edge_type = edge_types.get(direction, "hembra")
                
                edges.append({
                    "edgeId": edge_id,
                    "type": edge_type
                })
                
                neighbor_code = edge_neighbors.get(direction, "").strip() or None
                neighbors.append({
                    "edgeId": edge_id,
                    "neighborCode": neighbor_code
                })
        
        try:
            piece: Piece = add_piece(puzzle.id, code, sector, edges, neighbors)
            
            # Actualizar conexiones bidireccionales
            for neighbor in neighbors:
                if neighbor["neighborCode"]:
                    # Obtener la pieza vecina
                    neighbor_piece = get_piece(puzzle.id, neighbor["neighborCode"])
                    if neighbor_piece:
                        # Determinar la dirección opuesta
                        current_direction = EDGE_TO_DIRECTION[neighbor["edgeId"]]
                        opposite_direction = OPPOSITE_DIRECTION[current_direction]
                        opposite_edge_id = DIRECTION_TO_EDGE[opposite_direction]
                        
                        # Verificar si ya existe la conexión inversa
                        has_reverse = False
                        for nb in neighbor_piece.neighbors:
                            if nb.edgeId == opposite_edge_id and nb.neighborCode == code:
                                has_reverse = True
                                break
                        
                        # Si no existe, sugerir actualización
                        if not has_reverse:
                            st.info(f"💡 Sugerencia: La pieza **{neighbor['neighborCode']}** debería tener una conexión " 
                                   f"en su lado **{opposite_direction}** hacia **{code}**.")
            
            st.success(f"✔️ Pieza **{piece.code}** guardada correctamente.")
            
            # Limpiar estado de edición
            if "editing_piece" in st.session_state:
                del st.session_state["editing_piece"]
                
        except Exception as e:
            st.error(f"Error al guardar la pieza: {e}")

        # Refrescar lista y reiniciar la app
        refresh_existing()
        st.rerun()
    
    # Mostrar visualización simplificada del grafo de piezas
    if existing:
        st.markdown("---")
        st.subheader("📊 Visualización del Puzzle")
        st.info("Esta visualización muestra las conexiones entre piezas mapeadas hasta ahora.")
        
        # Código para generar un gráfico simple de conexiones entre piezas
        # (Se podría implementar con networkx+matplotlib o con st.graphviz_chart)
        connections = []
        for piece in existing:
            for neighbor in piece.neighbors:
                if neighbor.neighborCode:
                    direction = EDGE_TO_DIRECTION.get(neighbor.edgeId, f"C{neighbor.edgeId}")
                    connections.append(f"{piece.code} -- {direction} --> {neighbor.neighborCode}")
        
        if connections:
            st.code("\n".join(connections), language="")
        else:
            st.write("Aún no hay conexiones entre piezas.")
