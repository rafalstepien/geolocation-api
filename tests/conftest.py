import pytest
from database.database_client import DatabaseClient
from tests.utils import load_test_json_data
from ipstack_client.models import IpstackStandardLookupResponseModel


@pytest.fixture
def create_engine_mock(mocker):
    return mocker.patch(
        "database.database_client.create_engine"
    )


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
def test_ipstack_response_data():
    return load_test_json_data("ipstack_response.json")


@pytest.fixture
def test_ipstack_response_object(test_ipstack_response_data):
    return IpstackStandardLookupResponseModel(**test_ipstack_response_data)
