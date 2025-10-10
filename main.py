from enum import Enum

from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="La API en FastAPI de Víctor",
    version='20.32.65'
)


class Tags(Enum):
    items = "Inicio"


# @app.get("/", tags=[Tags.items])
@app.get("/", tags=['Inicio2'])
def read_root():
    return {"Hello": "World"}
