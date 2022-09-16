import pytest


@pytest.fixture
def create_engine_mock(mocker):
    return mocker.patch(
        "database.database_client.create_engine"
    )
