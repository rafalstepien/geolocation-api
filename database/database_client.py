from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from database.converters import IpstackToPostgresDataConverter
from database.models import UserInformation
from geolocation_api.error_handler.error_handler import handle_errors
from geolocation_api.ipstack_client.models import IpstackStandardLookupResponseModel
from geolocation_api.security import get_password_hash


class DatabaseClient:
    """
    Class responsible for communication with the database.
    """

    def __init__(self, user: str, password: str, host: str, database: str, port: int):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = str(port)

        self.connection_string = f"postgresql://{self.user}:{password}@{host}/{database}"
        self.engine = create_engine(self.connection_string)

    def create_user(self, username: str, password: str) -> None:
        """
        Create new entry in the User table.
        """
        user = UserInformation(username=username, password_hash=get_password_hash(password))
        self._insert_data_to_the_database([user])

    def get_user(self, username: str) -> UserInformation:
        """
        Query the database for a user with specified username
        """
        return Session(self.engine).query(UserInformation).filter_by(username=username).first()

    def upload_data(self, data: IpstackStandardLookupResponseModel) -> None:
        """
        Create new entry in geolocation_data and location_data tables.
        """
        converted_data = IpstackToPostgresDataConverter().convert(data)
        self._insert_data_to_the_database([converted_data])

    def delete_data(self, ip_address: str) -> None:
        pass

    def retrieve_data(self) -> None:
        pass

    def _insert_data_to_the_database(self, elements_to_add_to_session: Iterable) -> None:
        """
        Iterate over passed array and add all objects to the database.
        """
        with handle_errors(OperationalError):
            with Session(self.engine) as session:
                for element in elements_to_add_to_session:
                    session.add(element)
                session.commit()
