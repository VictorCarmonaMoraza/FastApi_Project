from pathfix import *
from utils.tags import Tags
from models.movie import Movie as ModelMovie
from bd.database import Session
from bearer_jwt import BearerJWT
from movieclass import Movie
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, Path, Query, status


routerMovie = APIRouter()


# GET
@routerMovie.get("/movies", tags=[Tags.movies], dependencies=[Depends(BearerJWT())])
def get_movies():
    db = Session()
    movies = db.query(ModelMovie).all()

    return JSONResponse(content=jsonable_encoder(movies), status_code=status.HTTP_200_OK)


@routerMovie.get("/movie/{id}", tags=[Tags.movies], status_code=status.HTTP_200_OK)
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"message": "No se ha encontrado la película"},
                            status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(data), status_code=status.HTTP_200_OK)


@routerMovie.get("/movies/", tags=[Tags.movies])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    db = Session()
    category = db.query(ModelMovie).filter(
        ModelMovie.category == category).all()
    if not category:
        return JSONResponse(content={"message": "No se han encontrado películas en esa categoría"},
                            status_code=status.HTTP_404_NOT_FOUND)
    return JSONResponse(content=jsonable_encoder(category), status_code=status.HTTP_200_OK)

# POST


@routerMovie.post("/movies", tags=[Tags.movies])
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

# PUT


@routerMovie.put('/movies/{id}', tags=[Tags.movies])
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

# DELETE


@routerMovie.delete('/movies/{id}', tags=[Tags.movies])
def delete_movie(id: int):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(content={"message": "No se ha encontrado la película"},
                            status_code=status.HTTP_404_NOT_FOUND)
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message": "Película eliminada correctamente", 'data': jsonable_encoder(data)},
                        status_code=status.HTTP_200_OK)
