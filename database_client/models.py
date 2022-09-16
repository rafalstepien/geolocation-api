from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship

from config_loader.config_loader import config

Base = declarative_base()
engine = create_engine(
    f"postgresql://"
    f"{config.HEROKU_POSTGRES_USER}:"
    f"{config.HEROKU_POSTGRES_PASSWORD}@"
    f"{config.HEROKU_POSTGRES_HOST}/"
    f"{config.HEROKU_POSTGRES_DATABASE}"
)


class LocationData(Base):
    __tablename__ = "location_data"

    id = Column(Integer, primary_key=True)

    geoname_id = Column(Integer)
    capital = Column(String)
    calling_code = Column(String)

    geolocation_data_id = Column(Integer, ForeignKey("geolocation_data.id"))

    def __repr__(self):
        return f"<LocationData({self.geoname_id})>"


class GeneralInformationData(Base):
    __tablename__ = "geolocation_data"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    hostname = Column(String)
    country_code = Column(String)
    region_code = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    location_data = relationship("LocationData", uselist=False, backref="geolocation_data")

    def __repr__(self):
        return f"<GeneralInformationData({self.ip_address})>"


Base.metadata.create_all(engine)
