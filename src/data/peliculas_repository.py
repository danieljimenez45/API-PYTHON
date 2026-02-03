from sqlmodel import Session, select
from src.models.pelicula import Pelicula


class PeliculasRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_peliculas(self) -> list[Pelicula]:
        peliculas = self.session.exec(select(Pelicula)).all()
        return peliculas 

    def get_pelicula(self, pelicula_id: int) -> Pelicula | None:
        pelicula =  self.session.get(Pelicula, pelicula_id)
        return pelicula

    def create_pelicula(self, pelicula: Pelicula) -> Pelicula:
        self.session.add(pelicula)
        self.session.commit()
        self.session.refresh(pelicula)
        return pelicula

    def update_pelicula(self, pelicula_id: int, pelicula_data: dict) -> Pelicula:
        pelicula = self.get_pelicula(pelicula_id)
        for key, value in pelicula_data.items():
            setattr(pelicula, key, value)
        self.session.commit()
        self.session.refresh(pelicula)
        return pelicula

    def delete_pelicula(self, pelicula_id: int) -> None:
        pelicula = self.get_pelicula(pelicula_id)
        self.session.delete(pelicula)
        self.session.commit()
