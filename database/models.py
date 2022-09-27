from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


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

    location_information_id = Column(Integer, ForeignKey("location_information.id"))
    location_information = relationship("LocationInformation", back_populates="general_information")

    def __repr__(self):
        return f"<GeneralInformationData({self.ip_address})>"


class LocationInformation(Base):
    __tablename__ = "location_information"

    id = Column(Integer, primary_key=True)

    geoname_id = Column(Integer)
    capital = Column(String)
    calling_code = Column(String)
    is_eu = Column(Boolean)
    country_flag_emoji = Column(String)

    language = relationship("Language", back_populates="location_information")
    general_information = relationship("GeneralInformation", back_populates="location_information", uselist=False)

    def __repr__(self):
        return f"<LocationInformation({self.geoname_id})>"


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    native = Column(String)

    location_information_id = Column(Integer, ForeignKey("location_information.id"))
    location_information = relationship("LocationInformation", back_populates="language")
