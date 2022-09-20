from database.database_client import DatabaseClient
from database.models import Base
from geolocation_api.config_loader.config_loader import config

database_client = DatabaseClient(
    user=config.HEROKU_POSTGRES_USER,
    password=config.HEROKU_POSTGRES_PASSWORD,
    host=config.HEROKU_POSTGRES_HOST,
    database=config.HEROKU_POSTGRES_DATABASE,
    port=config.HEROKU_POSTGRES_PORT,
)

Base.metadata.create_all(database_client.engine)

database_client.create_user(
    config.TEST_USER_USERNAME,
    config.TEST_USER_PASSWORD,
)
