import ipaddress

import pytest
from fastapi.exceptions import HTTPException
from requests import Response

from geolocation_api.ipstack_client.ipstack_client import IpstackClient


def test_get_data_for_ip_address_parses_data_correctly(
    mocker, raw_ipstack_response, ipstack_response_object, ip_address
):
    mocker.patch("requests.get", return_value=raw_ipstack_response)

    assert IpstackClient().get_data_for_ip_address(ip_address) == ipstack_response_object


def test_get_data_for_ip_address_raises_ipstack_api_error(mocker, raw_ipstack_response_with_empty_ip, ip_address):
    mocker.patch("requests.get", return_value=raw_ipstack_response_with_empty_ip)

    with pytest.raises(HTTPException) as e:
        IpstackClient().get_data_for_ip_address(ip_address)

    assert e.value.status_code == 503
    assert "ip" in e.value.detail


def test_ipstack_client_handles_connection_error_correctly(mocker, ipstack_error_response_data, ip_address):
    mocker.patch("requests.get", return_value=ipstack_error_response_data)

    with pytest.raises(HTTPException) as error:
        IpstackClient().get_data_for_ip_address(ip_address)

    assert error.value.status_code == 400
    assert error.value.detail == "Your monthly API request volume has been reached. Please upgrade your plan."


def test_ipstack_client_raises_correct_exception_for_response_not_in_json_format(mocker, ip_address):
    response = Response()
    response._content = b"<h1>RESPONSE IN HTML FORMAT</h1>"

    mocker.patch("requests.get", return_value=response)

    with pytest.raises(HTTPException) as e:
        IpstackClient().get_data_for_ip_address(ip_address)

    assert "Please check the response content" in e.value.detail


@pytest.mark.parametrize(
    "address",
    [
        "123.3.4.5",
        "interia.pl",
        "",
    ],
)
def test_convert_url_to_ip_address(mocker, raw_ipstack_response, address):
    mocker.patch("requests.get", return_value=raw_ipstack_response)
    assert ipaddress.ip_address(IpstackClient().convert_url_to_ip_address(address))
