from jwt import encode, decode

from config import SECRET_KEY


def createToken(data:dict):
    token:str= encode(payload=data,key=SECRET_KEY, algorithm='HS256')
    return token