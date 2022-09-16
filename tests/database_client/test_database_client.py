import pytest
from sqlalchemy.exc import OperationalError

from database.database_client import Session
from error_handler.exceptions import InvalidDatabaseCredentialsError


def test_database_client_initializes_correctly(create_engine_mock, test_database_client):
    assert test_database_client.connection_string == "postgresql://testuser:testpassword@127.0.0.1/testdatabase"
    assert create_engine_mock.called


def test_upload_data_inserts_to_database(mocker, create_engine_mock, test_database_client, ipstack_response_object):
    session_add_mock = mocker.patch.object(Session, "add")
    session_commit_mock = mocker.patch.object(Session, "commit")
    test_database_client.upload_data(ipstack_response_object)

    assert session_add_mock.called
    assert session_commit_mock.called


def test_client_handles_database_connection_error_correctly(
    mocker, create_engine_mock, test_database_client, ipstack_response_object
):
    mocker.patch.object(Session, "add")
    mocker.patch.object(Session, "commit", side_effect=OperationalError("", "", ""))

    with pytest.raises(InvalidDatabaseCredentialsError) as error:
        test_database_client.upload_data(ipstack_response_object)

    assert error.value.status_code == 401
