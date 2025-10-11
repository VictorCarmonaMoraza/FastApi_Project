from enum import Enum

from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="My FastAPI Application",
    description="La API en FastAPI de Víctor",
    version='20.32.65'
)


class Tags(Enum):
    movies = "Get Movies"
    movieId = "Get Movie by ID"
    moviesCreate = "Create Movie"


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


@app.get("/movie/{id}", tags=[Tags.movieId])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return []


@app.get("/movies/", tags=[Tags.moviesCreate])
def get_movies_by_category(category: str):
    return category


@app.post('/movies', tags=[Tags.moviesCreate])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(),
                 rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return title


@app.post("/movies2", tags=["Movies"])
def create_movie2(
        id: int,
        title: str,
        overview: str,
        year: int,
        rating: float,
        category: str
):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return {
        "message": f"Película '{title}' creada correctamente.",
        "movies": movies
    }


@app.put('/movies/{id}', tags=["Movies"])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(),
                 rating: float = Body(), category: str = Body()):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
            return movie
    return {"message": "Película no encontrada"}


@app.delete('/movies/{id}', tags=["Movies"])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return {"message": "Película eliminada correctamente"}
    return {"message": "Película no encontrada"}
