## API-PYTHON – Gestión de Películas (Ejercicio 3)

Repositorio para la realización de una API en Python con **FastAPI**, **SQLModel** y **MySQL**, con contenedores Docker tanto para la aplicación como para la base de datos.

Incluye:
- Repositorio en GitHub (rama ejercicio 3): `https://github.com/danieljimenez45/API-PYTHON/tree/EJERCICIO-3`
- API REST completa (`/api/peliculas`) con operaciones CRUD.
- Vistas HTML con plantillas Jinja2 para navegación web.
- Persistencia en **MySQL** usando Docker (`docker-compose.yml` / `docker-compose-env.yml`).
- Configuración mediante variables de entorno (`.env`).

---

## Base de datos y docker-compose (MySQL)

En el ejercicio 3 la base de datos principal es **MySQL** y se orquesta con Docker.

Los archivos de `docker-compose` son:

- `docker-compose.yml`: levanta la aplicación FastAPI (`fastapi-app`) y la base de datos MySQL (`fastapi-db-peliculas`) con credenciales fijas.
- `docker-compose-env.yml`: variante que toma las credenciales de la base de datos desde el archivo `.env` mediante variables de entorno.

En `docker-compose.yml` y `docker-compose-env.yml`:

- Servicio **fastapi-app**:
  - Construye la imagen usando el `Dockerfile` del proyecto.
  - Expone el puerto `8000` del contenedor al `8000` del host.
  - En `docker-compose.yml` monta el volumen `./src:/app` para desarrollo en caliente.
  - Depende de `fastapi-db`.

- Servicio **fastapi-db**:
  - Usa la imagen oficial de **MySQL**.
  - Configura `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD` (ya sea en claro o desde `.env`).
  - Expone el puerto `3306`.

En `data/db.py`:
- Se carga `.env` con `load_dotenv()`.
- Se construye la URL de conexión a MySQL (`mysql+pymysql://...`).
- La función `init_db()`:
  - Hace `drop_all` y `create_all` sobre el `engine`.
  - Inserta 5 películas de ejemplo.

---

## Configuración de variables de entorno

El archivo `.env` define las variables necesarias para conectarse a la base de datos y se usa junto con `docker-compose-env.yml` para inyectarlas en el contenedor MySQL.

Variables más habituales:

- **DB_NAME**: nombre de la base de datos (por defecto `peliculasdb`).
- **DB_USER**: usuario de la base de datos (por defecto `quevedo`).
- **DB_PASSWORD**: contraseña del usuario de la base de datos.
- **DB_PORT**: puerto de la base de datos (por defecto `3306` para MySQL, `5432` si se usa la parte de ejemplo de PostgreSQL).
- **DB_SERVER**: host/servicio de la base de datos (por defecto `fastapi-db` / `fastapi-db-peliculas` según el compose).
- **DB_URL**: URL de conexión completa para SQLAlchemy/SQLModel (permite sobreescribir la URL generada a partir de las variables anteriores).

En `data/db.py` se construye `DATABASE_URL` a partir de estas variables usando el dialecto `mysql+pymysql://…`, y se permite sobreescribirla directamente con `DB_URL` si está definida.

> **Importante:** no subir `.env` con credenciales reales a repositorios públicos; usarlo solo como plantilla de desarrollo.

---

## Tecnologías utilizadas

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **SQLModel** (sobre SQLAlchemy)
- **MySQL** (ejercicio 3)
- **Jinja2** (plantillas HTML)
- **Docker & Docker Compose**
- **pymysql**, **python-dotenv**, **python-multipart**, **cryptography**

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
├── docker-compose.yml
├── docker-compose-env.yml
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
- `data/db.py`: configuración de la base de datos MySQL, creación del `engine`, sesión (`get_session`) y función `init_db()` que crea las tablas y rellena datos de ejemplo.
- `data/peliculas_repository.py`: capa de acceso a datos (CRUD) para el modelo `Pelicula` usando `Session` de SQLModel.
- `models/pelicula.py`: definiciones del modelo de dominio (`Pelicula`), DTOs (`PeliculaCreate`, `PeliculaUpdate`, `PeliculaResponse`) y funciones de mapeo.
- `routers/api_peliculas_router.py`: router de FastAPI con todas las rutas de la API REST para películas.
- `templates/` + `static/`: vistas HTML (Jinja2) y recursos estáticos (CSS) para la parte web.

---

## Modelos y DTOs

En `models/pelicula.py` se definen:

- **Modelo de tabla** (`Pelicula`):  
  Representa la entidad película en la base de datos (campos: `id`, `titulo`, `genero`, `duracion`, `sinopsis`, `actores_principales`, `actores_secundarios`, `director`).

- **DTOs**:
  - `PeliculaCreate`: datos necesarios para crear una nueva película.
  - `PeliculaUpdate`: todos los campos opcionales para actualizaciones parciales.
  - `PeliculaResponse`: representación de salida para la API.

- **Mappers**:
  - `map_pelicula_to_response`
  - `map_create_to_pelicula`

---

## Repositorio de datos

En `data/peliculas_repository.py` se implementa la lógica de acceso a datos usando `Session`:

- `get_all_peliculas()`: devuelve una lista de todas las películas.
- `get_pelicula(pelicula_id)`: devuelve una película por `id` o `None` si no existe.
- `create_pelicula(pelicula)`: inserta y devuelve la película creada.
- `update_pelicula(pelicula_id, pelicula_data)`: aplica cambios a una película existente.
- `delete_pelicula(pelicula_id)`: elimina una película por `id`.

---

## Rutas de la API

El archivo `src/routers/api_peliculas_router.py` define un router con prefijo `/api/peliculas` y tag `peliculas`.

### Endpoints principales

- **GET `/api/peliculas/`** → lista de películas (`PeliculaResponse`).
- **POST `/api/peliculas/`** → creación de película (`PeliculaCreate` → `PeliculaResponse`, código `201`).
- **GET `/api/peliculas/{pelicula_id}`** → detalle por `id` (404 si no existe).
- **DELETE `/api/peliculas/{pelicula_id}`** → borrado (204 si todo va bien, 404 si no existe).
- **PATCH `/api/peliculas/{pelicula_id}`** → actualización parcial (`PeliculaUpdate`).
- **PUT `/api/peliculas/{pelicula_id}`** → reemplazo completo (`PeliculaCreate`).

---

## Rutas HTML y plantillas

En `main.py` se configuran:

- Montaje de estáticos: `app.mount("/static", StaticFiles(directory="static"), name="static")`.
- Plantillas Jinja2: `templates = Jinja2Templates(directory="templates")`.
- Inclusión del router de API: `app.include_router(api_peliculas_router)`.

### Rutas HTML

- **GET `/`**  
  Devuelve `index.html` (página principal).

- **GET `/peliculas`**  
  Lista todas las películas y renderiza `peliculas/peliculas.html`.

- **GET `/peliculas/new`**  
  Muestra el formulario `peliculas/pelicula_form.html` para crear una película.

- **POST `/pelicula/new`**  
  Procesa el formulario, crea una película y redirige a `/peliculas`.

- **GET `/peliculas/{pelicula_id}`**  
  Muestra el detalle de una película en `peliculas/pelicula_detalle.html` (404 si no existe).

---

## Instalación y ejecución en local (sin Docker)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/danieljimenez45/API-PYTHON.git
   cd API-PYTHON
   git checkout EJERCICIO-3
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
   - Ajustar `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SERVER`, `DB_PORT` según tu entorno local.

5. **Levantar MySQL (si no usas Docker, necesitarás tenerlo instalado y crear la base de datos con los datos del `.env`).**

6. **Ejecutar la aplicación**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 3006 --reload
   ```

7. **Probar en el navegador**
   - Web HTML:
     - `http://localhost:3006/`
     - `http://localhost:3006/peliculas`
   - Documentación de la API:
     - `http://localhost:3006/docs`
     - `http://localhost:3006/redoc`

---

## Ejecución con Docker + docker-compose (MySQL)

1. **Asegúrate de tener Docker y Docker Compose instalados.**

2. **Opción A – Usar credenciales fijas (`docker-compose.yml`)**
   ```bash
   docker compose up --build
   # En arranques posteriores:
   docker compose up
   ```

3. **Opción B – Usar variables de entorno (`docker-compose-env.yml`)**
   - Configura el archivo `.env` con las credenciales de la base de datos.
   ```bash
   docker compose -f docker-compose-env.yml up --build
   # En arranques posteriores:
   docker compose -f docker-compose-env.yml up
   ```

4. **Acceso a la aplicación en Docker**
   - Aplicación FastAPI: `http://localhost:8000/`
   - Documentación Swagger: `http://localhost:8000/docs`
   - Redoc: `http://localhost:8000/redoc`

5. **Parar los contenedores**
   ```bash
   docker compose down
   # o, si usas el compose con env:
   docker compose -f docker-compose-env.yml down
   ```

---
