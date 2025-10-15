
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from bd.database import engine, Base
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


@app.get("/")
def read_root():
    return HTMLResponse('<h2>Welcome to my API</h2>')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
