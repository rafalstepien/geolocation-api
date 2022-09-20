from pydantic import BaseModel


class Error(BaseModel):
    code: int
    type: str
    info: str


class IpstackErrorResponseModel(BaseModel):
    success: bool
    error: Error
