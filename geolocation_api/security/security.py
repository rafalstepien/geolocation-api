from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from jose import JWTError, jwt
from passlib.context import CryptContext

from database.models import UserInformation
from geolocation_api.config_loader import config
from geolocation_api.security import JWTData


class SecurityHandler:

    api_key_scheme = APIKeyHeader(name="Authorization")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION = 360  # minutes
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def decode_jwt_authorization_header(authorization_header: str = Depends(api_key_scheme)) -> JWTData:
        """
        Extract the token from the authorization header and try to decode it using the secret.
        """
        authorization_headers = authorization_header.split(" ")
        if len(authorization_headers) != 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = authorization_headers[1]
        try:
            decoded_token = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[SecurityHandler.JWT_ALGORITHM])
            return JWTData(**decoded_token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Decode failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def encode_jwt_token(payload: dict) -> str:
        """
        Create and sign JWT token based on provided payload.
        """
        exp = datetime.utcnow() + timedelta(minutes=SecurityHandler.JWT_EXPIRATION)
        return jwt.encode({**payload, "exp": exp}, config.JWT_SECRET_KEY, algorithm=SecurityHandler.JWT_ALGORITHM)

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        """
        Check if passed raw password after hashing equals hashed password.
        """
        return SecurityHandler.pwd_context.verify(raw_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Transform raw password to hash in order to store it in the database.
        """
        return SecurityHandler.pwd_context.hash(password)

    @staticmethod
    def authenticate_user(user: UserInformation, password: str) -> UserInformation:
        """
        Check if the user exists and if the passed password matches the one from database.
        If everything is right, then return this user.

        Args:
            user: User object from the database.
            password: Password passed by client when requesting the token.

        Returns:
            User object.
        """
        if not user:
            raise HTTPException(detail="Username is incorrect.", status_code=status.HTTP_401_UNAUTHORIZED)
        if not SecurityHandler.verify_password(password, user.password_hash):
            raise HTTPException(detail="Password is incorrect.", status_code=status.HTTP_401_UNAUTHORIZED)
        return user
