

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from user_jwt import createToken
from userclass import User
from utils.tags import Tags


routerUser = APIRouter()


@routerUser.post('/login', tags=[Tags.auth])
def login(user: User):
    if user.email == "victor" and user.password == "1234":
        token: str = createToken(user.model_dump())
        print(f'token: {token}')
        return JSONResponse(content={"token": token}, status_code=status.HTTP_200_OK)
    return JSONResponse(content={"message": "Credenciales inválidas"}, status_code=status.HTTP_401_UNAUTHORIZED)


@routerUser.get('/token', tags=[Tags.auth])
def get_token(email: str = Query(), password: str = Query()):
    user = User(email=email, password=password)
    token: str = createToken(user.model_dump())
    return JSONResponse(content={"token": token})
