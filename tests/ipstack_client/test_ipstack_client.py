import pytest
from requests import Response

from geolocation_api.error_handler.exceptions import IpstackAPIValueError, IpstackError
from geolocation_api.ipstack_client.ipstack_client import IpstackClient


def test_get_data_for_ip_address_parses_data_correctly(
    mocker, raw_ipstack_response, ipstack_response_object, ip_address
):
    mocker.patch("requests.get", return_value=raw_ipstack_response)

    assert IpstackClient().get_data_for_ip_address(ip_address) == ipstack_response_object


def test_get_data_for_ip_address_raises_ipstack_api_error(mocker, raw_ipstack_response_with_empty_ip, ip_address):
    mocker.patch("requests.get", return_value=raw_ipstack_response_with_empty_ip)

    with pytest.raises(IpstackAPIValueError):
        IpstackClient().get_data_for_ip_address(ip_address)


def test_ipstack_client_handles_connection_error_correctly(mocker, ipstack_error_response_data, ip_address):
    mocker.patch("requests.get", return_value=ipstack_error_response_data)

    with pytest.raises(IpstackError) as error:
        IpstackClient().get_data_for_ip_address(ip_address)

    assert error.value.status_code == 104
    assert error.value.message == "Your monthly API request volume has been reached. Please upgrade your plan."


def test_ipstack_client_raises_correct_exception_for_response_not_in_json_format(mocker, ip_address):
    response = Response()
    response._content = b"<h1>RESPONSE IN HTML FORMAT</h1>"

    mocker.patch("requests.get", return_value=response)

    with pytest.raises(IpstackError) as e:
        IpstackClient().get_data_for_ip_address(ip_address)

    assert "Please check the response content" in e.value.message
