from fastapi import Depends, FastAPI, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from config_loader.config_loader import config
from database.database_client import DatabaseClient
from geolocation_api.models import JWTData, TokenResponseModel
from geolocation_api.security import authenticate_user, decode_jwt_authorization_header, encode_jwt_token
from ipstack_client.ipstack_client import IpstackClient

app = FastAPI()
ipstack_client = IpstackClient()
database_client = DatabaseClient(
    user=config.HEROKU_POSTGRES_USER,
    password=config.HEROKU_POSTGRES_PASSWORD,
    host=config.HEROKU_POSTGRES_HOST,
    database=config.HEROKU_POSTGRES_DATABASE,
    port=config.HEROKU_POSTGRES_PORT,
)


@app.get("/data")
def get_data(ip_address: str):
    return {"endpoint": "get_data"}


@app.post("/data")
def add_data(ip_address: str, jwt_data: JWTData = Depends(decode_jwt_authorization_header)):
    data = ipstack_client.get_data_for_ip_address(ip_address)
    database_client.upload_data(data)
    return Response(status_code=status.HTTP_201_CREATED)


@app.delete("/data")
def delete_data(ip_address: str):
    return {"endpoint": "delete_data"}


@app.post("/token")
def post_credentials_to_obtain_jwt_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = database_client.get_user(form_data.username)
    authenticate_user(user, form_data.password)
    return TokenResponseModel(token=encode_jwt_token({"username": user.username}))
