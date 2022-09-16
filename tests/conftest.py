import json
from unittest.mock import Mock

import pytest

from database.database_client import DatabaseClient
from ipstack_client.models import IpstackStandardLookupResponseModel
from tests.utils import load_test_json_data


@pytest.fixture
def ip_address():
    return "123.45.67.8.9"


@pytest.fixture
def create_engine_mock(mocker):
    return mocker.patch("database.database_client.create_engine")


@pytest.fixture
def test_database_client():
    return DatabaseClient(
        user="testuser",
        password="testpassword",
        host="127.0.0.1",
        database="testdatabase",
        port=2137,
    )


@pytest.fixture
def ipstack_response_data():
    return load_test_json_data("ipstack_response.json")


@pytest.fixture
def ipstack_response_object(ipstack_response_data):
    return IpstackStandardLookupResponseModel(**ipstack_response_data)


@pytest.fixture
def raw_ipstack_response(ipstack_response_data):
    return Mock(content=json.dumps(ipstack_response_data).encode("utf-8"))


@pytest.fixture
def raw_ipstack_response_with_empty_ip(ipstack_response_data):
    ipstack_response_data["ip"] = None
    return Mock(content=json.dumps(ipstack_response_data).encode("utf-8"))


@pytest.fixture
def ipstack_error_response_data():
    return Mock(content=json.dumps(load_test_json_data("ipstack_error_response.json")).encode("utf-8"))
