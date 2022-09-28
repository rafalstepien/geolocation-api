import pytest

from database.models import GeneralInformation, Languages, LocationInformation
from geolocation_api.converters import DatabaseResponseConverter, IpstackResponseConverter


@pytest.mark.parametrize(
    "attribute, expected_value",
    [
        ("ip_address", "2601:5c2:201:2e30:f490:683d:2029:ce5f"),
        ("country_code", "US"),
        ("country_name", "United States"),
        ("region_name", "Virginia"),
    ],
)
def test_ipstack_response_converter_converts_correctly(ipstack_response_object, attribute, expected_value):
    converted = IpstackResponseConverter.convert(ipstack_response_object)
    assert getattr(converted, attribute) == expected_value


def test_database_response_converter_converts_correctly(ipstack_response_object):
    general_information_data = GeneralInformation(
        ip_address="2601:5c2:201:2e30:f490:683d:2029:ce5f",
        country_code="US",
        country_name="United States",
        region_code="VA",
        region_name="Virginia",
        city="Charlottesville",
        zip="22911",
        latitude=38.09666061401367,
        longitude=-78.3994369506836,
        location_information=LocationInformation(
            geoname_id=4752031,
            capital="Washington D.C.",
            calling_code="1",
            is_eu=False,
            languages=[
                Languages(
                    code="en",
                    name="English",
                    native="English",
                )
            ],
        ),
    )

    assert DatabaseResponseConverter.convert(general_information_data) == ipstack_response_object
