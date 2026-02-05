## API-PYTHON – Gestión de Películas

Proyecto de ejemplo con **FastAPI** y **SQLModel** para gestionar un catálogo de películas.  
Incluye:
- Repositorio en GitHub: `https://github.com/danieljimenez45/API-PYTHON`
- API REST completa (`/api/peliculas`) con operaciones CRUD.
- Vistas HTML con plantillas Jinja2 para navegación web.
- Persistencia en **PostgreSQL** con contenedores Docker y `docker-compose`.
- Configuración mediante variables de entorno (`.env`).
- Despliegue en Render accesible en: `https://api-python-62ja.onrender.com/`

---

## Tecnologías utilizadas

- **Python 3.13**
- **FastAPI**
- **Uvicorn**
- **SQLModel** (sobre SQLAlchemy)
- **PostgreSQL 16**
- **Jinja2** (plantillas HTML)
- **Docker & Docker Compose**
- **psycopg2-binary**, **python-dotenv**, **python-multipart**, **cryptography**

---

## Ramas del repositorio

Este proyecto está organizado en varias ramas de GitHub, cada una correspondiente a distintos ejercicios:

- **Rama ejercicios 1 y 2**:  
  `https://github.com/danieljimenez45/API-PYTHON/tree/EJERCICIOS-1%262`

- **Rama ejercicio 3**:  
  `https://github.com/danieljimenez45/API-PYTHON/tree/EJERCICIO-3`

- **Rama ejercicio 4 (rama actual)**:  
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

El archivo `.env` define las variables necesarias para conectarse a PostgreSQL (normalmente usadas en conjunto con `docker-compose-postgre.yml`):

- **DB_NAME**: nombre de la base de datos (por defecto `peliculasdb`).
- **DB_USER**: usuario de la base de datos (por defecto `quevedo`).
- **DB_PASSWORD**: contraseña del usuario de la base de datos.
- **DB_PORT**: puerto de PostgreSQL (por defecto `5432`).
- **DB_SERVER**: host/servicio de la base de datos (por defecto `fastapi-db-peliculas` para Docker).
- **DB_URL**: URL de conexión completa para SQLAlchemy/SQLModel.

En `data/db.py` se construye `DATABASE_URL` a partir de estas variables, y se permite sobreescribirla directamente con `DB_URL` si está definida.

> **Importante:** en producción (por ejemplo, en Render) hay que definir estas variables en el panel de variables de entorno del proveedor, sin subir `.env` público si contiene credenciales reales.

---

## Base de datos y docker-compose

El archivo `docker-compose-postgre.yml` define dos servicios:

- **fastapi-app**  
  - Construye la imagen usando el `Dockerfile` del proyecto.  
  - Expone el puerto `8000`.  
  - Depende de `fastapi-db` (base de datos).

- **fastapi-db**  
  - Contenedor de **PostgreSQL 16**.  
  - Lee las variables `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` desde el entorno (mapeadas con `DB_NAME`, `DB_USER`, `DB_PASSWORD`).  
  - Expone el puerto `5432`.

En `data/db.py`:
- Se carga `.env` con `load_dotenv()`.
- Se construye la URL de conexión a PostgreSQL (`postgresql+psycopg2://...`).
- La función `init_db()`:
  - Hace `drop_all` y `create_all` sobre el `engine`.
  - Inserta 5 películas de ejemplo.

---

## Driver de PostgreSQL utilizado

Este proyecto usa **`psycopg2-binary`** como driver de PostgreSQL, tal y como se ve en `requirements.txt` y en la URL de conexión:

- En `requirements.txt`:
  - `psycopg2-binary`
- En `data/db.py`:
  - `DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"`

### ¿Por qué `psycopg2-binary`?

- **Instalación sencilla**:  
  `psycopg2-binary` incluye binarios precompilados, lo que evita tener que instalar librerías de desarrollo del sistema (como `libpq-dev`, `gcc`, etc.) en el entorno local o en la imagen Docker.

- **Compatibilidad con SQLAlchemy/SQLModel**:  
  Es uno de los drivers recomendados/clásicos para conectar SQLAlchemy (y por tanto SQLModel) con PostgreSQL, por lo que la integración es directa y estable.

- **Ideal para entornos de desarrollo y demos**:  
  Para un proyecto de ejemplo como este, la prioridad es que la instalación sea rápida y sin fricción en distintos sistemas operativos.

### ¿Por qué no otros drivers?

- **`psycopg2` (no binary)**:  
  Es la versión compilada “normal”. Requiere disponer de las dependencias de compilación del sistema (cabeceras de PostgreSQL, compilador C, etc.). En entornos de clase o equipos heterogéneos suele dar más problemas de instalación, mientras que `psycopg2-binary` funciona con un simple `pip install`.

- **Drivers basados en async, como `asyncpg`**:  
  Aunque son muy buenos para aplicaciones totalmente asíncronas, este proyecto usa el stack estándar síncrono de SQLModel/SQLAlchemy y `psycopg2`, lo que simplifica el ejemplo y lo hace más alineado con la documentación básica de estas librerías.

En resumen, **`psycopg2-binary`** se ha elegido por su facilidad de instalación, buena compatibilidad con SQLModel/SQLAlchemy y su idoneidad para este entorno.

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

## Ejecución con Docker + docker-compose

1. **Asegúrate de tener Docker y Docker Compose instalados.**

2. **Configura el archivo `.env`** con las credenciales de la base de datos (las mismas que usará `docker-compose-postgre.yml`).

3. **Levanta los servicios con docker-compose**
   ```bash
   docker compose -f docker-compose-postgre.yml up --build
   # En arranques posteriores (si no has cambiado código o dependencias):
   docker compose -f docker-compose-postgre.yml up
   ```

4. **Acceso a la aplicación**
   - Aplicación FastAPI: `http://localhost:8000/`
   - Documentación Swagger: `http://localhost:8000/docs`
   - Redoc: `http://localhost:8000/redoc`

5. **Parar los contenedores**
   ```bash
   docker compose -f docker-compose-postgre.yml down
   ```

---

## Despliegue en Render (visión general)

Hay dos aproximaciones principales:

- **Servicio Python** (Render gestiona el runtime):
  - Build command: `pip install -r requirements.txt`
  - Start command (recomendado con esta estructura):  
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port $PORT
    ```
  - Configurar variables de entorno en Render (`DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SERVER`, `DB_PORT`, `DB_URL` si se desea).

- **Servicio Docker** (Render usa el `Dockerfile`):
  - Tipo de servicio: **Docker**.
  - Render construye la imagen leyendo el `Dockerfile` de la raíz.
  - El comando de arranque se toma del `CMD` del `Dockerfile`.

En ambos casos, es importante que la base de datos PostgreSQL sea accesible desde Render (bien como base de datos gestionada de Render, bien como otro servicio Docker en la misma red, etc.) y que la URL de conexión se configure correctamente mediante variables de entorno.


