"""Authentication service for SmartERP.

This service handles all authentication-related business logic including
user registration, authentication, password management, and account security.
"""

from __future__ import annotations

from datetime import datetime
from passlib.context import CryptContext
from uuid import UUID

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
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Service for authentication and user account management operations."""

    def __init__(self, repository: UserRepository) -> None:
        """Initialize service with injected repository."""
        self.repository = repository
        self.max_failed_attempts = 5

    def hash_password(self, password: str) -> str:
        """Hash a plain text password using bcrypt.

        Args:
            password: Plain text password to hash.

        Returns:
            Bcrypt hash of the password.
        """
        return pwd_context.hash(password)

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a plain text password against a hash.

        Args:
            password: Plain text password to verify.
            password_hash: Bcrypt hash to verify against.

        Returns:
            True if password matches, False otherwise.
        """
        return pwd_context.verify(password, password_hash)

    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user with validation and password hashing.

        Business rules:
        - Username must be unique
        - Email must be unique
        - Employee code must be unique
        - Password must be hashed before saving

        Args:
            user_data: Validated user creation data from Pydantic schema.

        Returns:
            Created User SQLAlchemy model instance.

        Raises:
            DuplicateUsernameError: If username already exists.
            DuplicateEmailError: If email already exists.
            DuplicateEmployeeCodeError: If employee code already exists.
        """
        # Check username uniqueness
        if self.repository.username_exists(user_data.username):
            raise DuplicateUsernameError(
                f"User with username '{user_data.username}' already exists"
            )

        # Check email uniqueness
        if self.repository.email_exists(user_data.email):
            raise DuplicateEmailError(
                f"User with email '{user_data.email}' already exists"
            )

        # Check employee code uniqueness
        if self.repository.employee_code_exists(user_data.employee_code):
            raise DuplicateEmployeeCodeError(
                f"User with employee code '{user_data.employee_code}' already exists"
            )

        # Hash password before storage
        password_hash = self.hash_password(user_data.password)

        # Create User model instance
        user = User(
            company_id=user_data.company_id,
            employee_code=user_data.employee_code,
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            mobile=user_data.mobile,
            password_hash=password_hash,
            department=user_data.department,
            designation=user_data.designation,
            role=user_data.role,
        )

        return self.repository.create(user)

    def authenticate_user(self, username: str, password: str) -> User:
        """Authenticate a user with username and password.

        Business rules:
        - Verify username exists
        - Verify password matches
        - Reject inactive users
        - Reject locked users
        - Increment failed login attempts on failure
        - Lock account after 5 failed attempts
        - Reset failed attempts on successful login
        - Update last login timestamp

        Args:
            username: Username for authentication.
            password: Plain text password for authentication.

        Returns:
            Authenticated User SQLAlchemy model instance.

        Raises:
            InvalidCredentialsError: If username or password is invalid.
            AccountInactiveError: If user account is inactive.
            AccountLockedError: If user account is locked.
        """
        user = self.repository.get_by_username(username)
        if not user:
            raise InvalidCredentialsError("Invalid username or password")

        # Check if account is active
        if not user.is_active:
            raise AccountInactiveError("Account is inactive")

        # Check if account is locked
        if user.is_locked:
            raise AccountLockedError("Account is locked due to too many failed login attempts")

        # Verify password
        if not self.verify_password(password, user.password_hash):
            # Increment failed login attempts
            self.repository.increment_failed_login(user)

            # Lock account after max failed attempts
            if user.failed_login_attempts >= self.max_failed_attempts - 1:
                self.repository.lock_user(user)
                raise AccountLockedError(
                    f"Account locked after {self.max_failed_attempts} failed login attempts"
                )

            raise InvalidCredentialsError("Invalid username or password")

        # Successful login - reset failed attempts and update last login
        self.repository.reset_failed_login(user)
        self.repository.update_last_login(user)

        return user

    def change_password(
        self, user: User, old_password: str, new_password: str
    ) -> User:
        """Change user password with old password verification.

        Business rules:
        - Verify old password matches
        - Hash new password
        - Update password_changed_at timestamp

        Args:
            user: User SQLAlchemy model instance.
            old_password: Current password for verification.
            new_password: New password to set.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            InvalidPasswordError: If old password is incorrect.
        """
        # Verify old password
        if not self.verify_password(old_password, user.password_hash):
            raise InvalidPasswordError("Current password is incorrect")

        # Hash new password
        user.password_hash = self.hash_password(new_password)
        user.password_changed_at = datetime.utcnow()

        return self.repository.update(user)

    def reset_password(self, user_id: UUID, new_password: str) -> User:
        """Reset user password (admin operation).

        Business rules:
        - Hash new password
        - Unlock account
        - Reset failed login attempts

        Args:
            user_id: UUID of the user whose password is being reset.
            new_password: New password to set.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        # Hash new password
        user.password_hash = self.hash_password(new_password)
        user.password_changed_at = datetime.utcnow()

        # Unlock account and reset failed attempts
        if user.is_locked:
            self.repository.unlock_user(user)
        else:
            self.repository.reset_failed_login(user)

        return self.repository.update(user)

    def lock_account(self, user_id: UUID) -> User:
        """Lock a user account for security reasons.

        Args:
            user_id: UUID of the user to lock.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        return self.repository.lock_user(user)

    def unlock_account(self, user_id: UUID) -> User:
        """Unlock a user account.

        Args:
            user_id: UUID of the user to unlock.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        return self.repository.unlock_user(user)

    def activate_user(self, user_id: UUID) -> User:
        """Activate a user account.

        Args:
            user_id: UUID of the user to activate.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        return self.repository.activate_user(user)

    def deactivate_user(self, user_id: UUID) -> User:
        """Deactivate a user account.

        Args:
            user_id: UUID of the user to deactivate.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        return self.repository.deactivate_user(user)

    def update_last_login(self, user_id: UUID) -> User:
        """Update the last login timestamp for a user.

        Args:
            user_id: UUID of the user to update.

        Returns:
            Updated User SQLAlchemy model instance.

        Raises:
            UserNotFoundError: If user does not exist.
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User with id '{user_id}' not found")

        return self.repository.update_last_login(user)
