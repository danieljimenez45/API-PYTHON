from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlmodel import Session, select

from models.pelicula import (
    Pelicula,
    PeliculaCreate,
    PeliculaUpdate,
    PeliculaResponse,
    map_create_to_pelicula,
    map_pelicula_to_response,
)
from data.db import init_db, get_session
from data.peliculas_repository import PeliculasRepository
from routers.api_peliculas_router import router as api_peliculas_router

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(api_peliculas_router)

#Ruta para la página prncipal 

@app.get("/", response_class = HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/peliculas", response_class = HTMLResponse)
async def ver_peliculas(request: Request, session: SessionDep):
    repo = PeliculasRepository(session)
    peliculas = repo.get_all_peliculas()
    return templates.TemplateResponse("peliculas/peliculas.html", {"request": request, "peliculas": peliculas})


@app.get("/peliculas/new" , response_class= HTMLResponse)
async def nueva_pelicula_form(request: Request):
    """Formulario para añadir una pelicula nueva"""
    return templates.TemplateResponse("peliculas/pelicula_form.html",{
        "request": request,
        "pelicula": Pelicula()
    })

@app.post("/pelicula/new", response_class= HTMLResponse)
async def crear_pelicula(request: Request, session: SessionDep):
    """Crear una nueva pelicula desde el formulario"""
    form_data = await request.form()
    titulo = form_data.get("titulo")
    genero = form_data.get("genero")
    duracion = form_data.get("duracion")
    sinopsis = form_data.get("sinopsis")
    actores_principales = form_data.get("actores_principales")
    actores_secundarios = form_data.get("actores_secundarios")
    director = form_data.get("director")

    pelicula_create = PeliculaCreate(
        titulo = titulo,
        genero = genero,
        duracion = duracion,
        sinopsis = sinopsis,
        actores_principales = actores_principales,
        actores_secundarios = actores_secundarios,
        director = director
    )

    repo = PeliculasRepository(session)
    pelicula = map_pelicula_to_response(pelicula_create)
    repo.create_pelicula(pelicula)

    return RedirectResponse(url="/peliculas", status_code=303)


@app.get("/peliculas/{pelicula_id}", response_class = HTMLResponse)
async def pelicula_por_id_html(pelicula_id: int ,request: Request, session: SessionDep):
    repo = PeliculasRepository(session)
    pelicula_encontrada = repo.get_pelicula(pelicula_id)
    if not pelicula_encontrada:
        raise HTTPException(status_code=404, detail= "Pelicula no encontrada")
    pelicula_response = map_pelicula_to_response(pelicula_encontrada)
    return templates.TemplateResponse("peliculas/pelicula_detalle.html", {"request": request, "pelicula": pelicula_response })



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3006, reload=True)


# http://localhost:3006
# http://localhost:3006/peliculas  
