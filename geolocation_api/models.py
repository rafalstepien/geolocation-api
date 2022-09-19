from pydantic import BaseModel


class JWTData(BaseModel):
    username: str
