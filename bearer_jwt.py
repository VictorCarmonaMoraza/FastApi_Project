from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer

from user_jwt import validateToken


class BearerJWT(HTTPBearer):

    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if (data['email'] != "victor"):
            raise HTTPException(
                status_code=403, detail="Credenciales inválidas")
        return data
