from sqlmodel import create_engine, SQLModel, Session
from models.pelicula import Pelicula

db_user: str = "quevedo"  
db_password: str =  "1234"
db_server: str = "fastapi-db" 
db_port: int = 3306  
db_name: str = "peliculasdb"  

DATABASE_URL = f"mysql+pymysql://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        session.add(Pelicula(
            id=1,
            titulo="El Padrino",
            genero="Drama",
            duracion=175,
            sinopsis="La historia de la familia mafiosa Corleone",
            actores_principales="Marlon Brando, Al Pacino",
            actores_secundarios="James Caan, Robert Duvall",
            director="Francis Ford Coppola"
        ))
        session.add(Pelicula(
            id=2,
            titulo="Pulp Fiction",
            genero="Crimen",
            duracion=154,
            sinopsis="Historias entrelazadas de criminales en Los Angeles",
            actores_principales="John Travolta, Samuel L. Jackson",
            actores_secundarios="Uma Thurman, Bruce Willis",
            director="Quentin Tarantino"
        ))
        session.add(Pelicula(
            id=3,
            titulo="El Señor de los Anillos: La Comunidad",
            genero="Fantasía",
            duracion=178,
            sinopsis="Un hobbit emprende un viaje para destruir un anillo",
            actores_principales="Elijah Wood, Ian McKellen",
            actores_secundarios="Viggo Mortensen, Orlando Bloom",
            director="Peter Jackson"
        ))
        session.add(Pelicula(
            id=4,
            titulo="Matrix",
            genero="Ciencia Ficción",
            duracion=136,
            sinopsis="Un hacker descubre la verdad sobre su realidad",
            actores_principales="Keanu Reeves, Laurence Fishburne",
            actores_secundarios="Carrie-Anne Moss, Hugo Weaving",
            director="Lana y Lilly Wachowski"
        ))
        session.add(Pelicula(
            id=5,
            titulo="Interestelar",
            genero="Ciencia Ficción",
            duracion=169,
            sinopsis="Exploradores viajan por un agujero de gusano",
            actores_principales="Matthew McConaughey, Anne Hathaway",
            actores_secundarios="Jessica Chastain, Michael Caine",
            director="Christopher Nolan"
        ))
        session.commit()