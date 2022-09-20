from unittest.mock import Mock

import pytest
from fastapi.exceptions import HTTPException

from error_handler.exceptions import IncorrectPasswordError, UserNotFoundError
from geolocation_api.models import JWTData
from geolocation_api.security import (
    authenticate_user,
    decode_jwt_authorization_header,
    encode_jwt_token,
    verify_password,
)


@pytest.mark.freeze_time("2022-01-01 00:00:00")
def test_decode_header_returns_correct_token(test_auth_header, test_jwt_token_payload):
    assert decode_jwt_authorization_header(test_auth_header) == JWTData(**test_jwt_token_payload)


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
        decode_jwt_authorization_header(authorization_header)


@pytest.mark.freeze_time("2022-01-01 00:00:00")
def test_jwt_token_is_encoded_correctly(test_jwt_token_payload, test_auth_header):
    token = encode_jwt_token(test_jwt_token_payload)
    assert token == test_auth_header.split(" ")[1]


@pytest.mark.parametrize(
    "raw_password, is_equal",
    [
        ("password1", False),
        ("123", True),
    ],
)
def test_verify_password(test_password_hash, raw_password, is_equal):
    assert verify_password(raw_password, test_password_hash) == is_equal


def test_user_is_authenticated_correctly(test_password_hash):
    user = Mock(password_hash=test_password_hash)
    assert authenticate_user(user, "123")


@pytest.mark.parametrize("user_object, exception", [(None, UserNotFoundError), (Mock(), IncorrectPasswordError)])
def test_authenticate_user_raises_correct_exception(user_object, exception, request):
    if user_object:
        user_object.password_hash = request.getfixturevalue("test_password_hash")
    with pytest.raises(exception):
        authenticate_user(user_object, "wrong-password")
