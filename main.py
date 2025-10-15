from enum import Enum

from fastapi import Depends, FastAPI, Body, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

import Movie
from Movie import Movie
from User import User
from bearer_jwt import BearerJWT
from pydantic import BaseModel
from user_jwt import createToken
from bd.database import Session, engine, Base
from models.movie import Movie as ModelMovie

app = FastAPI(
    title="My FastAPI Application",
    description="La API en FastAPI de Víctor",
    version='20.32.65'
)

Base.metadata.create_all(bind=engine)


class Tags(Enum):
    movies = "Get Movies"
    movieId = "Get Movie by ID"
    moviesCreate = "Create Movie"
    auth = "Authentication"


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


@app.post('/login', tags=[Tags.auth])
def login(user: User):
    if user.email == "victor" and user.password == "1234":
        token: str = createToken(user.model_dump())
        print(f'token: {token}')
        return JSONResponse(content={"token": token}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Credenciales inválidas"}, status_code=status.HTTP_401_UNAUTHORIZED)


@app.get('/token', tags=[Tags.auth])
def get_token(email: str = Query(), password: str = Query()):
    user = User(email=email, password=password)
    token: str = createToken(user.model_dump())
    return JSONResponse(content={"token": token})

# @app.get("/", tags=[Tags.items])


@app.get("/", tags=['Inicio2'])
def read_root():
    return HTMLResponse('<h1>Hola Mundo</h1>')


@app.get("/movies", tags=[Tags.movies], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    movies = db.query(ModelMovie).all()

    return JSONResponse(content=jsonable_encoder(movies), status_code=status.HTTP_200_OK)


@app.get("/movie/{id}", tags=[Tags.movieId], status_code=status.HTTP_200_OK)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"message": "No se ha encontrado la película"},
                            status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@app.get("/movies/", tags=[Tags.movies])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return category


@app.post("/movies", tags=[Tags.movies])
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    db.refresh(newMovie)

    movie_dict = {
        "id": newMovie.id,
        "title": newMovie.title,
        "overview": newMovie.overview,
        "year": newMovie.year,
        "rating": newMovie.rating,
        "category": newMovie.category
    }

    return JSONResponse(content={
        "message": "Película agregada correctamente",
        "movie": movie_dict
    })


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
def update_movie(id: int, movie: Movie):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"message": "No se ha encontrado la película"},
                            status_code=status.HTTP_404_NOT_FOUND)
    # Actulizar pelicula
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    db.refresh(data)
    return JSONResponse(
        content={
            "message": "Película actualizada correctamente",
            "movie": {
                "id": data.id,
                "title": data.title,
                "overview": data.overview,
                "year": data.year,
                "rating": data.rating,
                "category": data.category
            }
        },
        status_code=status.HTTP_200_OK
    )

    return JSONResponse(
        content={
            "message": "Película no encontrada",
            "status": status.HTTP_404_NOT_FOUND
        },
        status_code=status.HTTP_404_NOT_FOUND
    )


@app.delete('/movies/{id}', tags=["Movies"])
def delete_movie(id: int):
    for item in movies:
        if item['id'] == id:
            movies.remove(item)
            return JSONResponse(content={"message": "Película eliminada correctamente"})
    return JSONResponse(content={"message": "Película no encontrada"})
