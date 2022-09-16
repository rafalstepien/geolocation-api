from database.database_client import DatabaseClient


def test_database_client_initializes_correctly(create_engine_mock):

    client = DatabaseClient(
        user="testuser",
        password="testpassword",
        host="127.0.0.1",
        database="testdatabase",
        port=2137,
    )

    assert client.connection_string == "postgresql://testuser:testpassword@127.0.0.1/testdatabase"
    assert create_engine_mock.called


def test_upload_data_inserts_to_database():
    pass


def test_client_handles_database_connection_error_correctly():
    pass
