from contextlib import contextmanager

from pydantic.error_wrappers import ValidationError

from error_handler.exceptions import IpstackAPIValueError


class ErrorHandler:
    """
    Class responsible for parsing errors.
    """

    def handle(self, error: Exception) -> None:
        """
        Check what kind of error is raised and trigger correct handling for that type of error.

        Args:
            error: Exception object.
        """
        if isinstance(error, ValidationError):
            self._handle_validation_error(error)

    @staticmethod
    def _handle_validation_error(error: ValidationError) -> None:
        """
        If validation error occurs then improve the error message and raise more apropriate error.

        Args:
            error: ValidationError object
        """
        errors = []
        for error_data in error.errors():
            field = error_data.get("loc")[0]
            message = f"Ipstack API returned incorrect value in the following field: {field}"
            errors.append(IpstackAPIValueError(message=message))

        raise errors[0]


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
