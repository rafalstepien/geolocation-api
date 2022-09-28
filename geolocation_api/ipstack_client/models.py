from typing import List, Optional

from pydantic import BaseModel


class IpstackBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True


class IpstackLanguageModel(IpstackBaseModel):
    code: str
    name: str
    native: str


class IpstackLocationInformationModel(IpstackBaseModel):
    geoname_id: Optional[int] = -1
    capital: str
    languages: List[IpstackLanguageModel]
    calling_code: str
    is_eu: bool


class IpstackGeneralInformationModel(IpstackBaseModel):
    ip: str
    country_code: Optional[str] = ""
    country_name: Optional[str] = ""
    region_code: Optional[str] = ""
    region_name: Optional[str] = ""
    city: Optional[str] = ""
    zip: Optional[str] = ""
    latitude: float
    longitude: float
    location: IpstackLocationInformationModel
    is_eu: Optional[bool]
