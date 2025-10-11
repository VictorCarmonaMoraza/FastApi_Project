from enum import Enum

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="My FastAPI Application",
    description="La API en FastAPI de Víctor",
    version='20.32.65'
)


class Tags(Enum):
    movies = "Get Movies"


movies = [
    {
        'id': 1,
        'title': 'El Padrino',
        'overview': "El Padrino es una película de 1972 dirigida por Francis Ford Coppola ...",
        'year': '1972',
        'rating': 9.2,
        'category': 'Crimen'
    }
]


# @app.get("/", tags=[Tags.items])
@app.get("/", tags=['Inicio2'])
def read_root():
    return HTMLResponse('<h1>Hola Mundo</h1>')


@app.get("/movies", tags=[Tags.movies])
def get_movies():
    return movies

@app.get("/movie/{id}", tags=[Tags.movies])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return []
