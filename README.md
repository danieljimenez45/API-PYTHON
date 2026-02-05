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
