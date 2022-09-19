from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)


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
