from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class UserInformation(Base):
    __tablename__ = "user_information"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)

    def __repr__(self):
        return f"<UserInformation({self.username})>"


class GeneralInformation(Base):
    __tablename__ = "general_information"

    id = Column(Integer, primary_key=True)
    ip_address = Column(String)
    country_code = Column(String)
    country_name = Column(String)
    region_code = Column(String)
    region_name = Column(String)
    city = Column(String)
    zip = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    location_information = relationship(
        "LocationInformation", back_populates="general_information", lazy="subquery", cascade="all,delete"
    )

    location_information_id = Column(Integer, ForeignKey("location_information.id"))

    def __repr__(self):
        return f"<GeneralInformation({self.ip_address})>"


class LocationInformation(Base):
    __tablename__ = "location_information"

    id = Column(Integer, primary_key=True)

    geoname_id = Column(Integer)
    capital = Column(String)
    calling_code = Column(String)
    is_eu = Column(Boolean)

    languages = relationship("Languages", back_populates="location_information", lazy="subquery", cascade="all,delete")
    general_information = relationship(
        "GeneralInformation",
        back_populates="location_information",
        uselist=False,
        lazy="subquery",
        cascade="all,delete",
    )

    def __repr__(self):
        return f"<LocationInformation({self.geoname_id})>"


class Languages(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    code = Column(String)
    name = Column(String)
    native = Column(String)

    location_information_id = Column(Integer, ForeignKey("location_information.id"))
    location_information = relationship(
        "LocationInformation", back_populates="languages", lazy="subquery", cascade="all,delete"
    )

    def __repr__(self):
        return f"<Languages({self.name})>"
