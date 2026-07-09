"""Pydantic schemas for the SmartERP User module.

These schemas are the API contract for user master data and authentication.
They are kept separate from the SQLAlchemy model so request and response
shapes can evolve without coupling to persistence details.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    """Common user fields shared by create, update, and response schemas."""

    employee_code: str = Field(
        ...,
        min_length=1,
        max_length=32,
        description="Unique employee code for HR and payroll integration.",
        examples=["EMP001"],
    )
    username: str = Field(
        ...,
        min_length=4,
        max_length=64,
        description="Unique username for login authentication.",
        examples=["john.doe"],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address for communication and password recovery.",
        examples=["john.doe@company.com"],
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's first name.",
        examples=["John"],
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="User's last name.",
        examples=["Doe"],
    )
    mobile: str | None = Field(
        default=None,
        max_length=20,
        description="Mobile number for two-factor authentication and notifications.",
        examples=["+91-9876543210"],
    )
    department: str | None = Field(
        default=None,
        max_length=100,
        description="Department name for organizational structure.",
        examples=["Finance"],
    )
    designation: str | None = Field(
        default=None,
        max_length=100,
        description="Job title or designation.",
        examples=["Senior Accountant"],
    )
    role: str = Field(
        default="USER",
        max_length=50,
        description="User role for access control.",
        examples=["USER"],
    )

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: Any) -> Any:
        """Normalize username to lowercase before validation."""

        if value is None:
            return value
        return str(value).strip().lower()


class UserCreate(UserBase):
    """Schema used when creating a new user record."""

    company_id: UUID = Field(
        ...,
        description="Company ID to which the user belongs.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="User password (will be hashed before storage).",
        examples=["SecurePass123!"],
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """Ensure password meets minimum security requirements."""

        if len(value) < 8:
            raise ValueError("password must be at least 8 characters long")
        return value


class UserUpdate(BaseModel):
    """Schema used for partial user updates."""

    model_config = ConfigDict(from_attributes=True)

    employee_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=32,
        description="Unique employee code for HR and payroll integration.",
    )
    username: str | None = Field(
        default=None,
        min_length=4,
        max_length=64,
        description="Unique username for login authentication.",
    )
    email: EmailStr | None = Field(
        default=None,
        description="Unique email address for communication and password recovery.",
    )
    first_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="User's first name.",
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="User's last name.",
    )
    mobile: str | None = Field(
        default=None,
        max_length=20,
        description="Mobile number for two-factor authentication and notifications.",
    )
    department: str | None = Field(
        default=None,
        max_length=100,
        description="Department name for organizational structure.",
    )
    designation: str | None = Field(
        default=None,
        max_length=100,
        description="Job title or designation.",
    )
    role: str | None = Field(
        default=None,
        max_length=50,
        description="User role for access control.",
    )
    is_active: bool | None = Field(
        default=None,
        description="Indicates whether the user account is active.",
    )
    is_locked: bool | None = Field(
        default=None,
        description="Indicates whether the user account is locked due to security reasons.",
    )
    is_superuser: bool | None = Field(
        default=None,
        description="Indicates whether the user has superuser privileges.",
    )

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: Any) -> Any:
        """Normalize username to lowercase before validation."""

        if value is None:
            return value
        return str(value).strip().lower()


class UserResponse(UserBase):
    """Schema returned after create, update, and fetch operations."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique user identifier.", examples=["550e8400-e29b-41d4-a716-446655440000"])
    company_id: UUID = Field(
        ...,
        description="Company ID to which the user belongs.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    is_active: bool = Field(
        ...,
        description="Indicates whether the user account is active.",
        examples=[True],
    )
    is_locked: bool = Field(
        ...,
        description="Indicates whether the user account is locked due to security reasons.",
        examples=[False],
    )
    is_superuser: bool = Field(
        ...,
        description="Indicates whether the user has superuser privileges.",
        examples=[False],
    )
    last_login: datetime | None = Field(
        default=None,
        description="Timestamp of the last successful login.",
    )
    created_at: datetime = Field(..., description="Record creation timestamp.")
    updated_at: datetime = Field(..., description="Record last update timestamp.")


class UserLogin(BaseModel):
    """Schema for user login authentication."""

    username: str = Field(
        ...,
        min_length=4,
        description="Username for authentication.",
        examples=["john.doe"],
    )
    password: str = Field(
        ...,
        min_length=1,
        description="User password for authentication.",
        examples=["SecurePass123!"],
    )


class ChangePassword(BaseModel):
    """Schema for changing user password when logged in."""

    old_password: str = Field(
        ...,
        min_length=1,
        description="Current password for verification.",
        examples=["OldPass123!"],
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password to set.",
        examples=["NewSecurePass123!"],
    )

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """Ensure new password meets minimum security requirements."""

        if len(value) < 8:
            raise ValueError("new_password must be at least 8 characters long")
        return value


class ResetPassword(BaseModel):
    """Schema for resetting user password (admin or recovery flow)."""

    user_id: UUID = Field(
        ...,
        description="User ID for whom to reset the password.",
        examples=["550e8400-e29b-41d4-a716-446655440000"],
    )
    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="New password to set for the user.",
        examples=["NewSecurePass123!"],
    )

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, value: str) -> str:
        """Ensure new password meets minimum security requirements."""

        if len(value) < 8:
            raise ValueError("new_password must be at least 8 characters long")
        return value


class UserSummary(BaseModel):
    """Lightweight schema for user summaries in lists and references."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique user identifier.", examples=["550e8400-e29b-41d4-a716-446655440000"])
    username: str = Field(
        ...,
        description="Username for login authentication.",
        examples=["john.doe"],
    )
    full_name: str = Field(
        ...,
        description="Full name of the user.",
        examples=["John Doe"],
    )
    role: str = Field(
        ...,
        description="User role for access control.",
        examples=["USER"],
    )
    is_active: bool = Field(
        ...,
        description="Indicates whether the user account is active.",
        examples=[True],
    )


class Token(BaseModel):
    """JWT token response schema."""

    access_token: str = Field(..., description="JWT access token for authentication.")
    refresh_token: str = Field(..., description="JWT refresh token for obtaining new access tokens.")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer').")


class LoginResponse(BaseModel):
    """Response schema for successful login."""

    user: UserResponse = Field(..., description="User information.")
    tokens: Token = Field(..., description="JWT access and refresh tokens.")

