"""Authentication API endpoints for SmartERP.

This module provides RESTful endpoints for user authentication including
registration, login, token refresh, logout, and password management.
"""

from typing import Annotated
from uuid import UUID
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.security import (
    TokenPayload,
    create_access_token,
    create_refresh_token,
    get_current_superuser,
    get_current_user,
    verify_refresh_token,
)
from app.database.session import get_db
from app.dependencies import get_company_repository
from app.exceptions import (
    AccountInactiveError,
    AccountLockedError,
    DuplicateEmailError,
    DuplicateEmployeeCodeError,
    DuplicateUsernameError,
    InvalidCredentialsError,
    InvalidPasswordError,
    UserNotFoundError,
)
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    ChangePassword,
    LoginResponse,
    ResetPassword,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """Provide a UserRepository instance."""

    return UserRepository(db)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    """Provide an AuthService instance."""

    return AuthService(repository)


@router.post(
    "/register",
    summary="Register a new user",
    description="Create a new user account with validation for unique username, email, and employee code.",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    service: Annotated[AuthService, Depends(get_auth_service)],
    company_repository: Annotated[CompanyRepository, Depends(get_company_repository)],
) -> UserResponse:
    """Register a new user account.

    Args:
        user_data: Validated user creation data.
        service: Injected authentication service.
        company_repository: Injected company repository for validation.

    Returns:
        Created user response.

    Raises:
        HTTPException: If validation fails or company does not exist.
    """
    # Verify company exists
    company = company_repository.get_by_id(user_data.company_id)
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id '{user_data.company_id}' not found",
        )

    try:
        user = service.register_user(user_data)
        return user
    except DuplicateUsernameError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except DuplicateEmailError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except DuplicateEmployeeCodeError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )

@router.post(
    "/token",
    summary="OAuth2 Token",
    response_model=Token,
)
def oauth2_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Token:

    try:
        user = service.authenticate_user(
            form_data.username,
            form_data.password,
        )

        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "company_id": str(user.company_id),
            "role": user.role,
        }

        # CREATE THE TOKENS
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    except AccountInactiveError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    except AccountLockedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Generate a new access token using a valid refresh token.",
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
def refresh_token(refresh_token: str) -> Token:
    """Refresh access token using refresh token.

    Args:
        refresh_token: Valid JWT refresh token.

    Returns:
        New access token and refresh token.

    Raises:
        HTTPException: If refresh token is invalid or expired.
    """
    try:
        payload = verify_refresh_token(refresh_token)

        # Create new tokens
        token_data = {
            "sub": payload.sub,
            "username": payload.username,
            "company_id": payload.company_id,
            "role": payload.role,
        }

        new_access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


@router.post(
    "/logout",
    summary="User logout",
    description="Logout current user (stateless JWT, ready for future blacklist implementation).",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> None:
    """Logout current user.

    Note: This is a stateless JWT implementation. The client should discard
    the tokens. Future implementations may include token blacklisting.

    Args:
        current_user: Current authenticated user from JWT token.
    """
    # Stateless logout - client discards tokens
    # Future: Implement token blacklist for immediate revocation
    pass


@router.get(
    "/me",
    summary="Get current user",
    description="Retrieve information about the currently authenticated user.",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_current_user_info(
    payload: Annotated[TokenPayload, Depends(get_current_user)],
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserResponse:
    """Get current authenticated user information.

    Args:
        payload: Token payload from JWT.
        repository: Injected user repository.

    Returns:
        Current user response.

    Raises:
        HTTPException: If user is not found.
    """
    user = repository.get_by_id(UUID(payload.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post(
    "/change-password",
    summary="Change password",
    description="Change password for the currently authenticated user.",
    status_code=status.HTTP_200_OK,
)
def change_password(
    password_data: ChangePassword,
    payload: Annotated[TokenPayload, Depends(get_current_user)],
    repository: Annotated[UserRepository, Depends(get_user_repository)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, str]:
    """Change password for current user.

    Args:
        password_data: Old and new password data.
        payload: Token payload from JWT.
        repository: Injected user repository.
        service: Injected authentication service.

    Returns:
        Success message.

    Raises:
        HTTPException: If old password is incorrect or user not found.
    """
    user = repository.get_by_id(UUID(payload.sub))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    try:
        service.change_password(user, password_data.old_password, password_data.new_password)
        return {"message": "Password changed successfully"}
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/reset-password",
    summary="Reset password (Superuser only)",
    description="Reset password for any user (superuser only).",
    status_code=status.HTTP_200_OK,
)
def reset_password(
    password_data: ResetPassword,
    payload: Annotated[TokenPayload, Depends(get_current_superuser)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, str]:
    """Reset password for a user (superuser only).

    Args:
        password_data: User ID and new password.
        payload: Token payload from JWT (must be superuser).
        service: Injected authentication service.

    Returns:
        Success message.

    Raises:
        HTTPException: If user not found or not authorized.
    """
    try:
        service.reset_password(password_data.user_id, password_data.new_password)
        return {"message": "Password reset successfully"}
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
