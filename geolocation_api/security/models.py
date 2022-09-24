from pydantic import BaseModel


class JWTData(BaseModel):
    username: str


class TokenResponseModel(BaseModel):
    token: str
