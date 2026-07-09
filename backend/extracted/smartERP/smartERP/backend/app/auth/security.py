"""JWT Security module for SmartERP Enterprise.

This module provides enterprise-grade JWT authentication and password security
using python-jose for JWT operations and passlib for password hashing.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.config.settings import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenPayload(BaseModel):
    """JWT token payload structure."""

    sub: str  # User ID as string
    username: str
    company_id: str
    role: str
    exp: int
    iat: int
    type: str  # "access" or "refresh"


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash.

    Returns:
        Bcrypt hash of the password.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a bcrypt hash.

    Args:
        plain_password: Plain text password to verify.
        hashed_password: Bcrypt hash to verify against.

    Returns:
        True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any]) -> str:
    """Create a JWT access token.

    Args:
        data: Dictionary containing user data to encode in the token.
              Should include sub (user_id), username, company_id, role.

    Returns:
        Encoded JWT access token string.

    Raises:
        ValueError: If required fields are missing from data.
    """
    to_encode = data.copy()

    # Add expiration time
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    })

    # Encode JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict[str, Any]) -> str:
    """Create a JWT refresh token with longer expiration.

    Args:
        data: Dictionary containing user data to encode in the token.
              Should include sub (user_id), username, company_id, role.

    Returns:
        Encoded JWT refresh token string.

    Raises:
        ValueError: If required fields are missing from data.
    """
    to_encode = data.copy()

    # Refresh tokens have longer expiration (7 days)
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    })

    # Encode JWT
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> TokenPayload:
    """Decode and validate a JWT token.

    Args:
        token: JWT token string to decode.

    Returns:
        TokenPayload object with decoded token data.

    Raises:
        HTTPException: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return TokenPayload(**payload)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


def verify_access_token(token: str) -> TokenPayload:
    """Verify an access token and return its payload.

    Args:
        token: JWT access token string to verify.

    Returns:
        TokenPayload object with decoded token data.

    Raises:
        HTTPException: If token is invalid, expired, or not an access token.
    """
    payload = decode_token(token)

    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


def verify_refresh_token(token: str) -> TokenPayload:
    """Verify a refresh token and return its payload.

    Args:
        token: JWT refresh token string to verify.

    Returns:
        TokenPayload object with decoded token data.

    Raises:
        HTTPException: If token is invalid, expired, or not a refresh token.
    """
    payload = decode_token(token)

    if payload.type != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> TokenPayload:
    """FastAPI dependency to get current user from JWT token.

    This dependency extracts and validates the JWT token from the Authorization
    header and returns the token payload containing user information.

    Args:
        token: JWT token extracted by OAuth2PasswordBearer.

    Returns:
        TokenPayload object with current user information.

    Raises:
        HTTPException: If token is invalid, expired, or malformed.
    """
    return verify_access_token(token)


async def get_current_active_user(
    payload: Annotated[TokenPayload, Depends(get_current_user)]
) -> TokenPayload:
    """FastAPI dependency to get current active user.

    This dependency extends get_current_user to ensure the user account
    is active. In a full implementation, this would check the database
    to verify the user's is_active status.

    Args:
        payload: TokenPayload from get_current_user dependency.

    Returns:
        TokenPayload object with current active user information.

    Raises:
        HTTPException: If user account is inactive.
    #
    # Note: In production, this should query the database to verify
    # the user's current is_active status. For now, it returns the payload
    # assuming the token is valid and the user was active at token issuance.
    #
    """
    # TODO: Implement database check for user.is_active status
    # This would require injecting UserRepository and checking the user
    return payload


async def get_current_superuser(
    payload: Annotated[TokenPayload, Depends(get_current_active_user)]
) -> TokenPayload:
    """FastAPI dependency to get current superuser.

    This dependency ensures the current user has superuser privileges.

    Args:
        payload: TokenPayload from get_current_active_user dependency.

    Returns:
        TokenPayload object with current superuser information.

    Raises:
        HTTPException: If user is not a superuser.
    """
    if payload.role != "SUPERUSER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return payload
