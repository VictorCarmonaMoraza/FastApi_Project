

from pathfix import *
from routers.user_router import routerUser
from routers.movie_router import routerMovie
from bd.database import engine, Base
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI
import sys
import os

# ✅ Asegura que Python reconozca los módulos locales (bd, routers, utils, etc.)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


app = FastAPI(
    title="My FastAPI Application",
    description="La API en FastAPI de Víctor",
    version='20.32.65'
)

# ✅ Incluye los routers
app.include_router(routerMovie)
app.include_router(routerUser)

# ✅ Crea las tablas si no existen
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return HTMLResponse('<h2>Welcome to my API</h2>')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
