from typing import List, Optional

from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        allow_population_by_field_name = True


class Language(Model):
    code: str
    name: str
    native: str


class Location(Model):
    geoname_id: Optional[int] = -1
    capital: str
    languages: List[Language]
    calling_code: str
    is_eu: bool


class IpstackStandardLookupResponseModel(Model):
    ip: str
    type: Optional[str] = ""
    country_code: Optional[str] = ""
    country_name: Optional[str] = ""
    region_code: Optional[str] = ""
    region_name: Optional[str] = ""
    city: Optional[str] = ""
    zip: Optional[str] = ""
    latitude: float
    longitude: float
    location: Location
