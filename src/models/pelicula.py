from sqlmodel import Field, SQLModel


class Pelicula(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str = Field(index=True, max_length=50)
    genero: str = Field(index=True, max_length=50)
    duracion: int = Field(index=True)
    sinopsis: str = Field(max_length=150)
    actores_principales: str = Field(index=True, max_length=100)
    actores_secundarios: str = Field( max_length=100)
    director: str = Field(index = True, max_length=50)


# DTOs
class PeliculaCreate(SQLModel):
    titulo: str
    genero: str
    duracion: int
    sinopsis: str
    actores_principales: str
    actores_secundarios: str
    director: str


class PeliculaUpdate(SQLModel):
    titulo: str | None = None
    genero: str | None = None
    duracion: int | None = None
    sinopsis: str | None = None
    actores_principales: str | None = None
    actores_secundarios: str | None = None
    director: str | None = None


class PeliculaResponse(SQLModel):
    id: int
    titulo: str
    genero: str
    duracion: int
    sinopsis: str
    actores_principales: str
    actores_secundarios: str
    director: str


# Mappers
def map_pelicula_to_response(pelicula: Pelicula) -> PeliculaResponse:
    return PeliculaResponse(
        id=pelicula.id,
        titulo=pelicula.titulo,
        genero=pelicula.genero,
        duracion=pelicula.duracion,
        sinopsis=pelicula.sinopsis,
        actores_principales=pelicula.actores_principales,
        actores_secundarios=pelicula.actores_secundarios,
        director=pelicula.director,
    )


def map_create_to_pelicula(pelicula_create: PeliculaCreate) -> Pelicula:
    return Pelicula(
        titulo=pelicula_create.titulo,
        genero=pelicula_create.genero,
        duracion=pelicula_create.duracion,
        sinopsis=pelicula_create.sinopsis,
        actores_principales=pelicula_create.actores_principales,
        actores_secundarios=pelicula_create.actores_secundarios,
        director=pelicula_create.director,
    )


def map_update_to_pelicula(pelicula_update: PeliculaUpdate) -> Pelicula:
    return Pelicula(
        titulo=pelicula_update.titulo,
        genero=pelicula_update.genero,
        duracion=pelicula_update.duracion,
        sinopsis=pelicula_update.sinopsis,
        actores_principales=pelicula_update.actores_principales,
        actores_secundarios=pelicula_update.actores_secundarios,
        director=pelicula_update.director,
    )