from fastapi import status

from geolocation_api.error_handler.exceptions import InvalidDatabaseCredentialsError

SQLALCHEMY_ERROR_MAP = {"e3q8": InvalidDatabaseCredentialsError}
IPSTACK_ERROR_CODES_MAP = {
    404: status.HTTP_404_NOT_FOUND,
    101: status.HTTP_401_UNAUTHORIZED,
    102: status.HTTP_401_UNAUTHORIZED,
    103: status.HTTP_400_BAD_REQUEST,
    104: status.HTTP_400_BAD_REQUEST,
    105: status.HTTP_401_UNAUTHORIZED,
    106: status.HTTP_400_BAD_REQUEST,
    301: status.HTTP_400_BAD_REQUEST,
    302: status.HTTP_400_BAD_REQUEST,
    303: status.HTTP_400_BAD_REQUEST,
}
