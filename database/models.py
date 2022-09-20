from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)

    code = Column(String)
    name = Column(String)
    native = Column(String)


class UserInformation(Base):
    __tablename__ = "user_information"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)


class GeneralInformation(Base):
    __tablename__ = "general_information"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    hostname = Column(String)
    country_code = Column(String)
    region_code = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    location_information = relationship("LocationInformation", uselist=False, backref="location_information")

    def __repr__(self):
        return f"<GeneralInformationData({self.ip_address})>"


class LocationInformation(Base):
    __tablename__ = "location_information"

    id = Column(Integer, primary_key=True)

    geoname_id = Column(Integer)
    capital = Column(String)
    calling_code = Column(String)

    geolocation_data_id = Column(Integer, ForeignKey(GeneralInformation.id))

    def __repr__(self):
        return f"<LocationInformation({self.geoname_id})>"
