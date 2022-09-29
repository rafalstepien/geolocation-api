from typing import List

from fastapi import status


class BaseGeolocationAPIError(Exception):
    """
    Base class to inherit from for all errors.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    message: str = "An error occurred."

    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

    def __str__(self):
        return str(
            {
                "status_code": self.status_code,
                "message": self.message,
            }
        )


class MultipleExceptionsError(Exception):
    """
    Base for all errors that raise multiple errors at the same time.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    errors: List[BaseGeolocationAPIError] = None

    def __init__(self, errors=None, status_code=None):
        if errors:
            self.errors = errors
        if status_code:
            self.status_code = status_code

        self.message = [str(error) for error in self.errors]

    def __str__(self):
        return str(
            {
                "status_code": self.status_code,
                "message": self.message,
            }
        )


class IpstackAPIValueError(BaseGeolocationAPIError):
    """
    Raised when Ipstack API returns 'None' for mandatory field.
    """

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    ...


class InvalidDatabaseCredentialsError(BaseGeolocationAPIError):
    """
    Raised when credentials for connecting to database are invalid.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    message = (
        "Something went wrong with connection credentials. Please check "
        "if host, database name, user and password are correct."
    )


class IpstackError(BaseGeolocationAPIError):
    ...


class UnknownError(BaseGeolocationAPIError):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Unknown error occurred"
