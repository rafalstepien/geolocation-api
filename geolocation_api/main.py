from fastapi import FastAPI, Response, status

from config_loader.config_loader import config
from database.database_client import DatabaseClient
from ipstack.ipstack_client import IpstackClient

app = FastAPI()
ipstack_client = IpstackClient()
database_client = DatabaseClient(
    user=config.HEROKU_POSTGRES_USER,
    password=config.HEROKU_POSTGRES_PASSWORD,
    host=config.HEROKU_POSTGRES_HOST,
    database=config.HEROKU_POSTGRES_DATABASE,
    port=config.HEROKU_POSTGRES_PORT,
)


@app.get("/get_data")
def get_data(ip_address: str):
    return {"endpoint": "get_data"}


@app.post("/add_data")
def add_data(ip_address: str):
    data = ipstack_client.get_data_for_ip_address(ip_address)
    database_client.upload_data(data)
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/delete_data")
def delete_data(ip_address: str):
    return {"endpoint": "delete_data"}
