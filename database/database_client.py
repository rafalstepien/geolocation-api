from typing import Iterable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database.converters import IpstackToPostgresDataConverter
from ipstack_client.models import IpstackStandardLookupResponseModel


class DatabaseClient:
    def __init__(self, user: str, password: str, host: str, database: str, port: int):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = str(port)

        self.connection_string = f"postgresql://{self.user}:{password}@{host}/{database}"
        self.engine = create_engine(self.connection_string)

    def upload_data(self, data: IpstackStandardLookupResponseModel) -> None:
        converted_data = IpstackToPostgresDataConverter().convert(data)
        self._session_insert_handler(converted_data)

    def delete_data(self, ip_address: str):
        pass

    def retrieve_data(self):
        pass

    def _session_insert_handler(self, elements_to_add_to_session: Iterable) -> None:
        with Session(self.engine) as session:
            for element in elements_to_add_to_session:
                session.add(element)
            session.commit()
