from sqlalchemy import create_engine

from ipstack.models import IpstackStandardLookupResponseModel


class DatabaseClient:
    def __init__(self, user: str, password: str, host: str, database: str, port: int):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = str(port)

        self.connection_string = f"postgresql://{self.user}:{password}@{host}/{database}"
        self.engine = create_engine(self.connection_string)

    def upload_data(self, data: IpstackStandardLookupResponseModel):
        pass

    def delete_data(self, ip_address: str):
        pass

    def retrieve_data(self):
        pass
