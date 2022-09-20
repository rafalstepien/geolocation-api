import os

from pydantic import BaseSettings


class ConfigLoader(BaseSettings):
    HEROKU_POSTGRES_HOST: str = ""
    HEROKU_POSTGRES_DATABASE: str = ""
    HEROKU_POSTGRES_USER: str = ""
    HEROKU_POSTGRES_PORT: int = 5432
    HEROKU_POSTGRES_PASSWORD: str = ""

    IPSTACK_ACCESS_KEY: str = ""

    JWT_SECRET_KEY: str = ""

    class Config:
        env_file = os.environ.get("ENV_FILE")


config = ConfigLoader()
