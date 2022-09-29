from contextlib import contextmanager
from json import JSONDecodeError

from fastapi.exceptions import HTTPException
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import OperationalError

from geolocation_api.error_handler.constants import IPSTACK_ERROR_CODES_MAP, SQLALCHEMY_ERROR_MAP
from geolocation_api.error_handler.exceptions import (
    IpstackAPIValueError,
    IpstackError,
    MultipleExceptionsError,
    UnknownError,
)
from geolocation_api.error_handler.models import IpstackErrorResponseModel


class ErrorHandler:
    """
    Class responsible for parsing errors.
    """

    def handle(self, error: Exception):
        """
        Check what kind of error is raised and trigger correct handling for that type of error.

        Args:
            error: Exception object.
        """
        if isinstance(error, ValidationError):
            error = self._handle_validation_error(error)
        elif isinstance(error, OperationalError):
            error = self._handle_sqlalchemy_error(error)
        elif isinstance(error, JSONDecodeError):
            error = self._handle_json_decode_error(error)
        else:
            error = UnknownError()

        raise HTTPException(status_code=error.status_code, detail=error.message)

    @staticmethod
    def _handle_validation_error(error: ValidationError):
        """
        If validation error occurs then improve the error message and return more apropriate error.

        Args:
            error: ValidationError object
        """
        errors = []

        for error_data in error.errors():
            field = error_data.get("loc")[0]
            message = f"Ipstack API returned incorrect value in the following field: {field}"
            errors.append(IpstackAPIValueError(message=message))

        if len(errors) > 1:
            return MultipleExceptionsError(errors=errors)
        return errors[0]

    @staticmethod
    def _handle_sqlalchemy_error(error: OperationalError):
        return SQLALCHEMY_ERROR_MAP.get(error.code)

    @staticmethod
    def handle_ipstack_error_response(response_as_dictionary: dict):
        ipstack_error = IpstackErrorResponseModel(**response_as_dictionary)
        raise HTTPException(
            status_code=IPSTACK_ERROR_CODES_MAP.get(ipstack_error.error.code), detail=ipstack_error.error.info
        )

    @staticmethod
    def _handle_json_decode_error(error: JSONDecodeError):
        return IpstackError(
            message="There was a problem with decoding Ipstack API response. Please check the response content."
        )


@contextmanager
def handle_errors(*expected_errors: Exception) -> None:
    """
    Wrapper for handling errors to simplify usage.

    Args:
        *expected_errors: Errors that are supposed to be parsed by ErrorHandler.
    """
    try:
        yield
    except expected_errors as err:
        ErrorHandler().handle(err)
