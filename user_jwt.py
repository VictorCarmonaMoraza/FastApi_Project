from jwt import encode, decode

from config import SECRET_KEY


def createToken(data: dict):
    token: str = encode(payload=data, key=SECRET_KEY, algorithm='HS256')
    return token


def validateToken(token: str) -> dict:
    data: dict = decode(token, key=SECRET_KEY, algorithms=['HS256'])
    return data
