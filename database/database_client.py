from typing import Iterable, Tuple

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from database.models import GeneralInformation, UserInformation
from geolocation_api.converters import IpstackResponseConverter
from geolocation_api.error_handler import handle_errors
from geolocation_api.ipstack_client.models import IpstackGeneralInformationModel
from geolocation_api.security import SecurityHandler


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
        user = UserInformation(username=username, password_hash=SecurityHandler.get_password_hash(password))
        self._insert_data_to_the_database([user])

    def get_user(self, username: str) -> UserInformation:
        """
        Query the database for a user with specified username
        """
        return Session(self.engine).query(UserInformation).filter_by(username=username).first()

    def upload_data(self, data: IpstackGeneralInformationModel) -> None:
        """
        Create new entry in geolocation_data and location_data tables.
        """
        converted_data = IpstackResponseConverter.convert(data)
        self._insert_data_to_the_database([converted_data])

    def delete_data(self, ip_address: str) -> None:
        """
        Delete records that match given IP address.

        Args:
            ip_address: IP address that will be used to filter the records.
        """
        pass

    def get_data(self, ip_address: str) -> Tuple:
        """
        Return records that match given IP address.
        Args:
            ip_address: IP address that will be used to filter the records.
            username:
        """
        return Session(self.engine).query(GeneralInformation).filter_by(ip_address=ip_address).first()

    def _insert_data_to_the_database(self, elements_to_add_to_session: Iterable) -> None:
        """
        Iterate over passed array and add all objects to the database.
        """
        with handle_errors(OperationalError):
            with Session(self.engine) as session:
                for element in elements_to_add_to_session:
                    session.add(element)
                session.commit()
