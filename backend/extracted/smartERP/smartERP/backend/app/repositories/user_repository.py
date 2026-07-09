"""User repository for database operations.

This repository handles all database interactions for the User entity.
It follows the Repository Pattern and contains no business logic or validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Repository for User entity database operations."""

    def __init__(self, db: Session) -> None:
        """Initialize repository with database session."""
        self.db = db

    def create(self, user: User) -> User:
        """Create a new user record.

        Args:
            user: User SQLAlchemy model instance to persist.

        Returns:
            The persisted User instance with generated id and timestamps.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by its primary key.

        Args:
            user_id: UUID of the user to retrieve.

        Returns:
            User instance if found, None otherwise.
        """
        stmt = select(User).where(User.id == user_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username.

        Args:
            username: Username for authentication.

        Returns:
            User instance if found, None otherwise.
        """
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email address.

        Args:
            email: Email address of the user.

        Returns:
            User instance if found, None otherwise.
        """
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_employee_code(self, employee_code: str) -> Optional[User]:
        """Retrieve a user by employee code.

        Args:
            employee_code: Unique employee code.

        Returns:
            User instance if found, None otherwise.
        """
        stmt = select(User).where(User.employee_code == employee_code)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_users(
        self,
        company_id: UUID | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        """Retrieve users with pagination support, optionally filtered by company.

        Args:
            company_id: Optional company ID to filter users.
            skip: Number of records to skip (offset).
            limit: Maximum number of records to return.

        Returns:
            List of User instances sorted by username ascending.
        """
        stmt = select(User).order_by(User.username.asc()).offset(skip).limit(limit)
        if company_id is not None:
            stmt = stmt.where(User.company_id == company_id)
        return list(self.db.execute(stmt).scalars().all())

    def update(self, user: User) -> User:
        """Update an existing user record.

        Args:
            user: User SQLAlchemy model instance with updated fields.

        Returns:
            The updated User instance.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> User:
        """Soft delete a user by setting is_active to False.

        Args:
            user: User SQLAlchemy model instance to soft delete.

        Returns:
            The updated User instance with is_active set to False.
        """
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def hard_delete(self, user: User) -> None:
        """Permanently delete a user record from the database.

        Reserved for Super Admin functionality. Use with extreme caution
        as this operation cannot be undone and may violate data integrity
        if the user has related records.

        Args:
            user: User SQLAlchemy model instance to delete permanently.
        """
        self.db.delete(user)
        self.db.commit()

    def activate_user(self, user: User) -> User:
        """Activate a user account by setting is_active to True.

        Args:
            user: User SQLAlchemy model instance to activate.

        Returns:
            The updated User instance with is_active set to True.
        """
        user.is_active = True
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def deactivate_user(self, user: User) -> User:
        """Deactivate a user account by setting is_active to False.

        Args:
            user: User SQLAlchemy model instance to deactivate.

        Returns:
            The updated User instance with is_active set to False.
        """
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def lock_user(self, user: User) -> User:
        """Lock a user account by setting is_locked to True.

        Args:
            user: User SQLAlchemy model instance to lock.

        Returns:
            The updated User instance with is_locked set to True.
        """
        user.is_locked = True
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def unlock_user(self, user: User) -> User:
        """Unlock a user account by setting is_locked to False.

        Args:
            user: User SQLAlchemy model instance to unlock.

        Returns:
            The updated User instance with is_locked set to False.
        """
        user.is_locked = False
        user.failed_login_attempts = 0
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_last_login(self, user: User) -> User:
        """Update the last login timestamp for a user.

        Args:
            user: User SQLAlchemy model instance to update.

        Returns:
            The updated User instance with last_login set to current time.
        """
        user.last_login = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def increment_failed_login(self, user: User) -> User:
        """Increment the failed login attempts counter for a user.

        Args:
            user: User SQLAlchemy model instance to update.

        Returns:
            The updated User instance with failed_login_attempts incremented.
        """
        user.failed_login_attempts += 1
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def reset_failed_login(self, user: User) -> User:
        """Reset the failed login attempts counter for a user.

        Args:
            user: User SQLAlchemy model instance to update.

        Returns:
            The updated User instance with failed_login_attempts reset to 0.
        """
        user.failed_login_attempts = 0
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return user

    def username_exists(self, username: str) -> bool:
        """Check if a user with the given username exists.

        Args:
            username: Username to check for existence.

        Returns:
            True if a user with the username exists, False otherwise.
        """
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def email_exists(self, email: str) -> bool:
        """Check if a user with the given email exists.

        Args:
            email: Email address to check for existence.

        Returns:
            True if a user with the email exists, False otherwise.
        """
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def employee_code_exists(self, employee_code: str) -> bool:
        """Check if a user with the given employee code exists.

        Args:
            employee_code: Employee code to check for existence.

        Returns:
            True if a user with the employee code exists, False otherwise.
        """
        stmt = select(User).where(User.employee_code == employee_code)
        return self.db.execute(stmt).scalar_one_or_none() is not None
