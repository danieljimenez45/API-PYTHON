from fastapi import APIRouter, HTTPException , Depends
from typing import Annotated
from src.models.pelicula import (
    PeliculaCreate,
    PeliculaUpdate,
    PeliculaResponse,
    map_create_to_pelicula,
    map_pelicula_to_response,
)
from src.data.peliculas_repository import PeliculasRepository
from sqlmodel import Session
from src.data.db import  get_session

router = APIRouter(prefix="/api/peliculas", tags= ["peliculas"])

SessionDep = Annotated[Session, Depends(get_session)]

#Rutas de la API para gestionar peliculas

@router.get("/", response_model=list[PeliculaResponse])
def lista_peliculas(session: SessionDep):
    repo = PeliculasRepository(session)
    peliculas = repo.get_all_peliculas()
    return [map_pelicula_to_response(p) for p in peliculas]


@router.post("/", response_model=PeliculaResponse, status_code=201)
def nueva_pelicula(pelicula_create: PeliculaCreate, session: SessionDep):
    repo = PeliculasRepository(session)
    pelicula = map_create_to_pelicula(pelicula_create)
    pelicula_creada = repo.create_pelicula(pelicula)
    return map_pelicula_to_response(pelicula_creada)


@router.get("/{pelicula_id}", response_model=PeliculaResponse)
def pelicula_por_id(pelicula_id: int, session: SessionDep):
    repo = PeliculasRepository(session)
    pelicula = repo.get_pelicula(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return map_pelicula_to_response(pelicula)


@router.delete("/{pelicula_id}", status_code=204)
def borrar_pelicula(pelicula_id: int, session: SessionDep):
    repo = PeliculasRepository(session)
    pelicula = repo.get_pelicula(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    repo.delete_pelicula(pelicula_id)


@router.patch("/{pelicula_id}", response_model=PeliculaResponse)
def actualizar_parcial_pelicula(
    pelicula_id: int,
    pelicula_update: PeliculaUpdate,
    session: SessionDep,
):
    repo = PeliculasRepository(session)
    pelicula_encontrada = repo.get_pelicula(pelicula_id)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    pelicula_data = pelicula_update.model_dump(exclude_unset=True)
    pelicula_actualizada = repo.update_pelicula(pelicula_id, pelicula_data)
    return map_pelicula_to_response(pelicula_actualizada)


@router.put("/{pelicula_id}", response_model=PeliculaResponse)
def reemplazar_pelicula(
    pelicula_id: int,
    pelicula_update: PeliculaCreate,
    session: SessionDep,
):
    repo = PeliculasRepository(session)
    pelicula = repo.get_pelicula(pelicula_id)
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    pelicula_data = pelicula_update.model_dump()
    pelicula_actualizada = repo.update_pelicula(pelicula_id, pelicula_data)
    return map_pelicula_to_response(pelicula_actualizada)
