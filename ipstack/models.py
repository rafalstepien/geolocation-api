from typing import List

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        allow_population_by_field_name = True


class Language(Model):
    code: str
    name: str
    native: str


class Location(Model):
    geoname_id: int
    capital: str
    languages: List[Language]
    calling_code: str
    is_eu: bool


class IpstackStandardLookupResponseModel(Model):
    ip: str
    type: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    city: str
    zip: str
    latitude: float
    longitude: float
    location: Location
