from unittest.mock import Mock

import pytest
from sqlalchemy.exc import OperationalError

from database.database_client import DatabaseClient, Session
from database.models import UserInformation
from geolocation_api.error_handler.exceptions import InvalidDatabaseCredentialsError
from geolocation_api.security import SecurityHandler


def test_database_client_initializes_correctly(create_engine_mock, test_database_client):
    assert test_database_client.connection_string == "postgresql://testuser:testpassword@127.0.0.1/testdatabase"
    assert create_engine_mock.called


def test_upload_data_inserts_to_database(mocker, create_engine_mock, test_database_client, ipstack_response_object):
    session_add_mock = mocker.patch.object(Session, "add")
    session_commit_mock = mocker.patch.object(Session, "commit")
    test_database_client.upload_data(ipstack_response_object)

    assert session_add_mock.called
    assert session_commit_mock.called


def test_get_user_works_correctly(mocker, test_database_client, test_username):
    session_query_mock = mocker.patch.object(Session, "query")
    test_database_client.get_user(test_username)
    assert session_query_mock.called


def test_get_data_works_correctly(mocker, test_database_client, ip_address):
    session_query_mock = mocker.patch.object(Session, "query")
    test_database_client.get_data(ip_address)
    assert session_query_mock.called


def test_client_handles_database_connection_error_correctly(
    mocker, create_engine_mock, test_database_client, ipstack_response_object
):
    mocker.patch.object(Session, "add")
    mocker.patch.object(Session, "commit", side_effect=OperationalError("", "", ""))

    with pytest.raises(InvalidDatabaseCredentialsError) as error:
        test_database_client.upload_data(ipstack_response_object)

    assert error.value.status_code == 401


def test_create_user(mocker, test_database_client, test_username):
    session_add_mock = mocker.patch.object(Session, "add")
    session_commit_mock = mocker.patch.object(Session, "commit")

    test_database_client.create_user(test_username, "test_password")

    assert session_add_mock.called_with(
        UserInformation(
            username=test_username,
            password_hash=SecurityHandler.get_password_hash("test_password"),
        )
    )
    assert session_commit_mock.called


def test_delete_data_works_correctly(mocker, test_database_client):
    session_delete_mock = mocker.patch.object(Session, "delete")
    session_commit_mock = mocker.patch.object(Session, "commit")
    mocker.patch.object(Session, "query")

    test_database_client.delete_data(Mock())

    assert session_delete_mock.called
    assert session_commit_mock.called


def test_validate_credentials_raises_error_for_incorrect_credentials(test_username):
    with pytest.raises(InvalidDatabaseCredentialsError):
        DatabaseClient(test_username, "tespassword", None, "database", "port")
