# Puzzle Mapper App

## Descripción

Puzzle Mapper es una aplicación web ligera que permite:

* **Registrar** rompecabezas de formas arbitrarias (incluso con piezas faltantes e "islas").
* **Mapear** cada pieza mediante una interfaz gráfica sencilla sin necesidad de coordenadas rígidas.
* **Generar** instrucciones paso a paso, claras y atómicas, para armar el rompecabezas desde cualquier pieza inicial.

Ideal para usuarios sin experiencia en armar rompecabezas, con un flujo guiado de captura y armado.

---

## Características

* Interfaz web con **Streamlit**: formularios interactivos para registro y mapeo de piezas.
* **MongoDB** como base de datos principal (Atlas o local) con modelo flexible.
* **Python** 3.x: toda la lógica, conexión y generación de instrucciones.
* Algoritmo de recorrido (DFS) que respeta "islas" y huecos.

---

## Estructura del Proyecto

```
puzzle_app/
├── app.py                      # Punto de entrada Streamlit
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Variables de entorno (MONGO_URI, DB_NAME, LOG_LEVEL)
├── configs/
│   └── config.py               # Carga de configuración
├── database/
│   ├── client.py               # Conexión singleton a MongoDB
│   └── repositories.py         # Funciones CRUD para puzzles y pieces
├── models/
│   ├── puzzle.py               # Modelo Pydantic de Puzzle
│   └── piece.py                # Modelo Pydantic de Piece
├── services/
│   ├── puzzle_service.py       # Lógica de negocio de puzzles y piezas
│   └── instruction_service.py  # Algoritmo de generación de instrucciones
├── ui/
│   ├── create_puzzle.py        # Formulario de creación de puzzles
│   ├── map_piece.py            # Formulario de mapeo de piezas
│   └── display_instructions.py # Vista de instrucciones de armado
├── utils/
│   ├── logger.py               # Configuración de logging
│   └── traversal.py            # Funciones genéricas de DFS
└── tests/                      # (Opcional) Pruebas unitarias e integración
```

---

## Requisitos Previos

* Python 3.8+ instalado.
* Cuenta en MongoDB Atlas o instancia local de MongoDB.
* Git para control de versiones.

---

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TU_USUARIO/puzzle-app.git
   cd puzzle-app
   ```
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuración

1. Renombra el archivo `.env.example` a `.env` y edítalo con tus credenciales:

   ```dotenv
   MONGO_URI=mongodb+srv://<usuario>:<contraseña>@<cluster>.mongodb.net
   DB_NAME=puzzle_db
   LOG_LEVEL=INFO
   ```
2. Verifica que los valores sean correctos.

---

## Uso

1. Ejecuta la aplicación Streamlit:

   ```bash
   streamlit run app.py
   ```
2. En el navegador, navega a `http://localhost:8501`.
3. En la barra lateral elige:

   * **Crear Puzzle**: ingresa nombre, cantidad de piezas y sectores.
   * **Mapear Piezas**: para cada pieza define sector, tipo de borde y vecino.
   * **Ver Instrucciones**: selecciona pieza inicial y genera pasos de armado.

---

## Arquitectura

* **Entry Point**: `app.py` maneja la navegación entre vistas.
* **UI**: carpeta `ui/` con componentes individuales.
* **Servicios**: carpeta `services/` con lógica de negocio y generación de instrucciones.
* **Data Access**: carpeta `database/` con repositorios CRUD.
* **Modelos**: carpeta `models/` con validación Pydantic.
* **Utilidades**: carpeta `utils/` para logging y algoritmos genéricos.

---

## Contribuciones

1. Fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza commits claros y descriptivos (**conventional commits**).
4. Abre un Pull Request describiendo tus cambios.


