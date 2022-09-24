from typing import Tuple

from database.models import GeneralInformation, LocationInformation
from geolocation_api.ipstack_client.models import IpstackStandardLookupResponseModel


class IpstackToPostgresDataConverter:
    @staticmethod
    def convert(
        ipstack_response_data: IpstackStandardLookupResponseModel,
    ) -> Tuple[GeneralInformation, LocationInformation]:
        """
        Convert data returned from ipstack_client.com to the format that is acceptable by database.

        Args:
            ipstack_response_data: Data returned by Ipstack API.

        Returns:
            Data converted to database tables objects.
        """
        general_information_data = GeneralInformation(
            ip_address=ipstack_response_data.ip,
            country_code=ipstack_response_data.country_code,
            region_code=ipstack_response_data.region_code,
            city=ipstack_response_data.city,
            zip=ipstack_response_data.zip,
            latitude=ipstack_response_data.latitude,
            longitude=ipstack_response_data.longitude,
        )
        location_information_data = LocationInformation(
            geoname_id=ipstack_response_data.location.geoname_id,
            capital=ipstack_response_data.location.capital,
            calling_code=ipstack_response_data.location.calling_code,
        )

        return general_information_data, location_information_data
