from database.models import Base
from config_loader.config_loader import config
from sqlalchemy import create_engine


engine = create_engine(
    f"postgresql://"
    f"{config.HEROKU_POSTGRES_USER}:"
    f"{config.HEROKU_POSTGRES_PASSWORD}@"
    f"{config.HEROKU_POSTGRES_HOST}/"
    f"{config.HEROKU_POSTGRES_DATABASE}"
)

Base.metadata.create_all(engine)
