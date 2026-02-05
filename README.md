## API-PYTHON – Gestión de Películas

Proyecto de ejemplo con **FastAPI** y **SQLModel** para gestionar un catálogo de películas.  
Incluye:
- Repositorio en GitHub: `https://github.com/danieljimenez45/API-PYTHON`
- API REST completa (`/api/peliculas`) con operaciones CRUD.
- Vistas HTML con plantillas Jinja2 para navegación web.
- Persistencia en **MySQL** (ejercicios 1 y 2) con contenedores Docker y `docker-compose`.
- Configuración mediante variables de entorno (`.env`).

---

## Tecnologías utilizadas

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **SQLModel** (sobre SQLAlchemy)
- **MySQL** (ejercicios 1 y 2)
- **Jinja2** (plantillas HTML)
- **Docker & Docker Compose**
- **pymysql**, **python-dotenv**, **python-multipart**, **cryptography**

---

## Ramas relacionadas

Este proyecto tiene varias ramas para distintos ejercicios:

- **Ejercicios 1 y 2**: `EJERCICIOS-1&2`
- **Ejercicio 3 (esta rama)**: `EJERCICIO-3`
- **Ejercicio 4 (PostgreSQL + Render)**: `EJERCICIO-4`

Cada rama tiene su propia configuración de base de datos y, en el caso del ejercicio 4, además despliegue en Render.

---

## Ramas del repositorio

Este proyecto está organizado en varias ramas de GitHub, cada una correspondiente a distintos ejercicios:

- **Rama ejercicios 1 y 2**:  
  `https://github.com/danieljimenez45/API-PYTHON/tree/EJERCICIOS-1%262`

- **Rama ejercicio 3**:  
  `https://github.com/danieljimenez45/API-PYTHON/tree/EJERCICIO-3`

- **Rama ejercicio 4**:  
  `https://github.com/danieljimenez45/API-PYTHON/tree/EJERCICIO-4`

---

## Estructura del proyecto

```text
.
├── Dockerfile
├── docker-compose-postgre.yml
├── requirements.txt
├── .env
└── src
    ├── main.py
    ├── data
    │   ├── db.py
    │   └── peliculas_repository.py
    ├── models
    │   └── pelicula.py
    ├── routers
    │   └── api_peliculas_router.py
    ├── templates
    │   ├── index.html
    │   ├── fragments
    │   │   └── base.html
    │   └── peliculas
    │       ├── peliculas.html
    │       ├── pelicula_detalle.html
    │       └── pelicula_form.html
    └── static
        └── css
            └── styles.css
```

- `main.py`: punto de entrada de la aplicación FastAPI (configura rutas HTML, monta estáticos, registra el router de la API y gestiona el ciclo de vida con `lifespan`).
- `data/db.py`: configuración de la base de datos, creación del `engine`, sesión (`get_session`) y función `init_db()` que crea las tablas y rellena datos de ejemplo.
- `data/peliculas_repository.py`: capa de acceso a datos (CRUD) para el modelo `Pelicula` usando `Session` de SQLModel.
- `models/pelicula.py`: definiciones del modelo de dominio (`Pelicula`), DTOs (`PeliculaCreate`, `PeliculaUpdate`, `PeliculaResponse`) y funciones de mapeo.
- `routers/api_peliculas_router.py`: router de FastAPI con todas las rutas de la API REST para películas.
- `templates/` + `static/`: vistas HTML (Jinja2) y recursos estáticos (CSS) para la parte web.

---

## Configuración de variables de entorno

El archivo `.env` define las variables necesarias para conectarse a la base de datos.  
En los **ejercicios 1 y 2** la configuración principal está orientada a **MySQL**, aunque también se incluyen ejemplos para PostgreSQL comentados.

Variables más habituales:

- **DB_NAME**: nombre de la base de datos (por defecto `peliculasdb`).
- **DB_USER**: usuario de la base de datos (por defecto `quevedo`).
- **DB_PASSWORD**: contraseña del usuario de la base de datos.
- **DB_PORT**: puerto de la base de datos (por defecto `3306` para MySQL).
- **DB_SERVER**: host/servicio de la base de datos (por defecto `localhost` o el nombre del servicio Docker).
- **DB_URL**: URL de conexión completa para SQLAlchemy/SQLModel (permite sobreescribir la URL generada a partir de las variables anteriores).

En `src/data/db.py` se construye `DATABASE_URL` a partir de estas variables, y se permite sobreescribirla directamente con `DB_URL` si está definida.

> **Importante:** no subir `.env` con credenciales reales a repositorios públicos; usarlo solo como plantilla de desarrollo.

---

## Base de datos y docker-compose

En los ejercicios 1 y 2 la base de datos principal es **MySQL**.

El archivo `docker-compose-mysql.yml` define el servicio de base de datos:

- **db-mysql**  
  - Imagen oficial de **MySQL**.  
  - Variables de entorno:
    - `MYSQL_ROOT_PASSWORD`
    - `MYSQL_DATABASE`
    - `MYSQL_USER`
    - `MYSQL_PASSWORD`
  - Expone el puerto `3306`.

La aplicación FastAPI se conecta a este contenedor mediante la URL de conexión construida en `src/data/db.py`.

En `src/data/db.py`:
- Se carga `.env` con `load_dotenv()`.
- Se construye la URL de conexión a MySQL (`mysql+pymysql://...`).
- La función `init_db()`:
  - Hace `drop_all` y `create_all` sobre el `engine`.
  - Inserta 5 películas de ejemplo.

---

## Driver de MySQL utilizado

Este proyecto usa **`pymysql`** como driver de MySQL, tal y como se ve en `requirements.txt` y en la URL de conexión:

- En `requirements.txt`:
  - `pymysql`
- En `src/data/db.py`:
  - `DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"`

---

## Modelos y DTOs

En `models/pelicula.py` se definen:

- **Modelo de tabla** (`Pelicula`):
  - Campos: `id`, `titulo`, `genero`, `duracion`, `sinopsis`, `actores_principales`, `actores_secundarios`, `director`.
  - Usa `SQLModel` con `table=True` para mapear a la tabla en la base de datos.

- **DTOs de entrada/salida**:
  - `PeliculaCreate`: datos necesarios para crear una nueva película.
  - `PeliculaUpdate`: todos los campos opcionales, para actualizaciones parciales (`PATCH`) o totales (`PUT`).
  - `PeliculaResponse`: representación de respuesta para exponer vía API.

- **Funciones de mapeo**:
  - `map_pelicula_to_response(pelicula: Pelicula) -> PeliculaResponse`
  - `map_create_to_pelicula(pelicula_create: PeliculaCreate) -> Pelicula`
  - `map_update_to_pelicula(pelicula_update: PeliculaUpdate) -> Pelicula`

---

## Repositorio de datos

En `data/peliculas_repository.py` se implementa la lógica de acceso a datos usando `Session`:

- `get_all_peliculas()`: devuelve una lista de todas las películas.
- `get_pelicula(pelicula_id)`: devuelve una película por `id` o `None` si no existe.
- `create_pelicula(pelicula)`: inserta y devuelve la película creada.
- `update_pelicula(pelicula_id, pelicula_data)`: aplica cambios a una película existente (usado por `PATCH` y `PUT`).
- `delete_pelicula(pelicula_id)`: elimina una película por `id`.

---

## Rutas de la API

El archivo `src/routers/api_peliculas_router.py` define un router con prefijo `/api/peliculas` y tag `peliculas`.  
Todas las rutas usan el repositorio y los DTOs para separar lógica de negocio y transporte.

### Endpoints principales

- **GET `/api/peliculas/`**  
  - Devuelve una lista de `PeliculaResponse`.  
  - Usa `PeliculasRepository.get_all_peliculas()`.

- **POST `/api/peliculas/`**  
  - Crea una nueva película a partir de un cuerpo `PeliculaCreate`.  
  - Respuesta: `PeliculaResponse` con código `201`.

- **GET `/api/peliculas/{pelicula_id}`**  
  - Devuelve una película por `id`.  
  - Si no existe: `HTTP 404` con mensaje `"Película no encontrada"`.

- **DELETE `/api/peliculas/{pelicula_id}`**  
  - Elimina una película por `id`.  
  - Si no existe: `HTTP 404`.  
  - Respuesta sin contenido (`204`).

- **PATCH `/api/peliculas/{pelicula_id}`**  
  - Actualización parcial con `PeliculaUpdate` (solo campos enviados).  
  - Si no existe: `HTTP 404`.  
  - Devuelve `PeliculaResponse` actualizada.

- **PUT `/api/peliculas/{pelicula_id}`**  
  - Reemplazo completo usando `PeliculaCreate`.  
  - Si no existe: `HTTP 404`.  
  - Devuelve `PeliculaResponse` resultante.

---

## Rutas HTML y plantillas

En `main.py` se configuran:

- Montaje de estáticos: `app.mount("/static", StaticFiles(directory="static"), name="static")`.
- Plantillas Jinja2: `templates = Jinja2Templates(directory="templates")`.
- Inclusión del router de API: `app.include_router(api_peliculas_router)`.

### Rutas HTML

- **GET `/`**  
  - Devuelve `index.html`.  
  - Página principal (inicio).

- **GET `/peliculas`**  
  - Obtiene todas las películas desde `PeliculasRepository`.  
  - Renderiza `peliculas/peliculas.html` con la lista.

- **GET `/peliculas/new`**  
  - Muestra formulario (`peliculas/pelicula_form.html`) para crear nueva película.

- **POST `/pelicula/new`**  
  - Lee los datos del formulario.  
  - Crea una `Pelicula` nueva y la guarda a través del repositorio.  
  - Redirige a `/peliculas` con código `303`.

- **GET `/peliculas/{pelicula_id}`**  
  - Muestra el detalle de una película en `peliculas/pelicula_detalle.html`.  
  - Si no existe: `HTTP 404`.

---

## Instalación y ejecución en local (sin Docker)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/danieljimenez45/API-PYTHON.git
   cd API-PYTHON
   ```

2. **Crear y activar un entorno virtual (opcional pero recomendado)**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # En Windows
   # o
   source .venv/bin/activate  # En Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   - Crear un archivo `.env` en la raíz (si no existe) basándote en el ejemplo incluido.  
   - Ajustar `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SERVER`, `DB_PORT` según tu entorno local o contenedor de base de datos.

5. **Levantar PostgreSQL (si no usas Docker, necesitarás tenerlo instalado y creando la base de datos manualmente con los datos del `.env`).**

6. **Ejecutar la aplicación**
   Desde la raíz del proyecto:
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 3006 --reload
   ```

7. **Probar en el navegador**
   - Web HTML:
     - `http://localhost:3006/`
     - `http://localhost:3006/peliculas`
   - Documentación interactiva de la API:
     - `http://localhost:3006/docs`
     - `http://localhost:3006/redoc`

---

## Ejecución con Docker + docker-compose (MySQL)

1. **Asegúrate de tener Docker y Docker Compose instalados.**

2. **Configura el archivo `.env`** con las credenciales de base de datos acordes a `docker-compose-mysql.yml` (nombre de BD, usuario, contraseña, etc.).

3. **Levanta el contenedor de MySQL con docker-compose**
   ```bash
   docker compose -f docker-compose-mysql.yml up --build
   # En arranques posteriores (si no has cambiado nada de la BD):
   docker compose -f docker-compose-mysql.yml up
   ```

4. **Ejecuta la aplicación FastAPI apuntando a ese MySQL**
   Desde la raíz del proyecto:
   ```bash
   uvicorn src.main:app --host 127.0.0.1 --port 3006 --reload
   ```

5. **Parar los contenedores MySQL**
   ```bash
   docker compose -f docker-compose-mysql.yml down
   ```

---
