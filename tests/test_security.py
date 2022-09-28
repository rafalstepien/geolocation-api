from unittest.mock import Mock

import pytest
from fastapi.exceptions import HTTPException

from geolocation_api.error_handler.exceptions import IncorrectPasswordError, UserNotFoundError
from geolocation_api.security import JWTData, SecurityHandler


@pytest.mark.freeze_time("2022-01-01 00:00:00")
def test_decode_header_returns_correct_token(test_auth_header, test_jwt_token_payload):
    assert SecurityHandler.decode_jwt_authorization_header(test_auth_header) == JWTData(**test_jwt_token_payload)


@pytest.mark.parametrize(
    "authorization_header",
    [
        "",
        "bearer that has too many elements",
        "Bearer invalidbearer",
    ],
)
def test_decode_header_raises_http_exception_for_incorrect_header(authorization_header):
    with pytest.raises(HTTPException):
        SecurityHandler.decode_jwt_authorization_header(authorization_header)


@pytest.mark.freeze_time("2022-01-01 00:00:00")
def test_jwt_token_is_encoded_correctly(test_jwt_token_payload, test_auth_header):
    token = SecurityHandler.encode_jwt_token(test_jwt_token_payload)
    assert token == test_auth_header.split(" ")[1]


@pytest.mark.parametrize(
    "raw_password, is_equal",
    [
        ("password1", False),
        ("123", True),
    ],
)
def test_verify_password(test_password_hash, raw_password, is_equal):
    assert SecurityHandler.verify_password(raw_password, test_password_hash) == is_equal


def test_user_is_authenticated_correctly(test_password_hash):
    user = Mock(password_hash=test_password_hash)
    assert SecurityHandler.authenticate_user(user, "123")


@pytest.mark.parametrize("user_object, exception", [(None, UserNotFoundError), (Mock(), IncorrectPasswordError)])
def test_authenticate_user_raises_correct_exception(user_object, exception, request):
    if user_object:
        user_object.password_hash = request.getfixturevalue("test_password_hash")
    with pytest.raises(exception):
        SecurityHandler.authenticate_user(user_object, "wrong-password")
