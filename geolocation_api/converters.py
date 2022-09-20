from abc import ABC, abstractmethod
from typing import Any

from database.models import GeneralInformation, Languages, LocationInformation
from geolocation_api.ipstack_client.models import (
    IpstackGeneralInformationModel,
    IpstackLanguageModel,
    IpstackLocationInformationModel,
)


class BaseConverter(ABC):
    """
    An interface for data converter.
    """

    @staticmethod
    @abstractmethod
    def convert(data: Any) -> Any:
        pass


class IpstackResponseConverter(BaseConverter):
    """
    Converts data returned by Ipstack API to the format accepted by SQL Alchemy.
    """

    @staticmethod
    def convert(data: IpstackGeneralInformationModel) -> GeneralInformation:
        """
        Convert data returned from Ipstack API to the format that is acceptable by the database.

        Args:
            data: Data returned by Ipstack API.

        Returns:
            Data converted to database tables objects.
        """
        general_information_data = GeneralInformation(
            ip_address=data.ip,
            country_code=data.country_code,
            country_name=data.country_name,
            region_code=data.region_code,
            region_name=data.region_name,
            city=data.city,
            zip=data.zip,
            latitude=data.latitude,
            longitude=data.longitude,
            location_information=LocationInformation(
                geoname_id=data.location.geoname_id,
                capital=data.location.capital,
                calling_code=data.location.calling_code,
                is_eu=data.location.is_eu,
                languages=[
                    Languages(
                        code=language.code,
                        name=language.name,
                        native=language.native,
                    )
                    for language in data.location.languages
                ],
            ),
        )

        return general_information_data


class DatabaseResponseConverter(BaseConverter):
    """
    Converts data returned by SQL Alchemy to the format similar to Ipstack API.
    """

    @staticmethod
    def convert(data: GeneralInformation) -> IpstackGeneralInformationModel:
        if data:
            return IpstackGeneralInformationModel(
                ip=data.ip_address,
                country_code=data.country_code,
                country_name=data.country_name,
                region_code=data.region_code,
                region_name=data.region_name,
                city=data.city,
                zip=data.zip,
                latitude=data.latitude,
                longitude=data.longitude,
                location=IpstackLocationInformationModel(
                    geoname_id=data.location_information.geoname_id,
                    capital=data.location_information.capital,
                    calling_code=data.location_information.calling_code,
                    is_eu=data.location_information.is_eu,
                    languages=[
                        IpstackLanguageModel(
                            code=language.code,
                            name=language.name,
                            native=language.native,
                        )
                        for language in data.location_information.languages
                    ],
                ),
            )
