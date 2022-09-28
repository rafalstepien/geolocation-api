import json
from unittest.mock import Mock

import pytest
from passlib.context import CryptContext

from database.database_client import DatabaseClient
from geolocation_api.ipstack_client.models import IpstackGeneralInformationModel
from tests.utils import load_test_json_data


@pytest.fixture(autouse=True)
def test_env(monkeypatch):
    monkeypatch.setattr("geolocation_api.config_loader.config_loader.config.JWT_SECRET_KEY", "secret")
    monkeypatch.setattr(
        "geolocation_api.security.security.SecurityHandler.pwd_context",
        CryptContext(schemes=["bcrypt"], deprecated="auto"),
    )


@pytest.fixture
def test_password_hash():
    return "$2b$12$842kgmlVOkHthiTiOh5C1.AXk.cVG0B/VT2aKwwk3UCN/mZL3NmAe"


@pytest.fixture
def test_jwt_token_payload():
    return {
        "username": "test_username",
        "exp": 1640998800,
    }


@pytest.fixture
def test_auth_header():
    return (
        "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJ1c2VybmFtZSI6InRlc3RfdXNlcm5hbWUiLCJleHAiOjE2NDEwMTY4MDB9."
        "s7ItLux8nLypmUzU-ynrG8us_MvVQ92lhlx2V5TOQGw"
    )


@pytest.fixture
def ip_address():
    return "123.45.67.8.9"


@pytest.fixture
def test_username():
    return "testuser"


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
    return IpstackGeneralInformationModel(**ipstack_response_data)


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
