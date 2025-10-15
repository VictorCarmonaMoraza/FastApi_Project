from enum import Enum

from fastapi import Depends, FastAPI, Body, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse

import movieclass
from movieclass import Movie
from userclass import User
from bearer_jwt import BearerJWT
from pydantic import BaseModel
from user_jwt import createToken
from bd.database import Session, engine, Base
from models.movie import Movie as ModelMovie
from utils.tags import Tags
from routers.movie_router import routerMovie
from routers.user_router import routerUser

app = FastAPI(
    title="My FastAPI Application",
    description="La API en FastAPI de Víctor",
    version='20.32.65'
)
app.include_router(routerMovie)
app.include_router(routerUser)

Base.metadata.create_all(bind=engine)
