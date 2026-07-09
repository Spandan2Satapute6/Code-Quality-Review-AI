"""User master model for SmartERP.

This entity represents application users who belong to a specific company.
All user records are scoped by company_id to maintain multi-tenancy.
Passwords are stored only as bcrypt hashes for security.
"""

from __future__ import annotations

from datetime import datetime
import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class User(Base):
    """User master record for authentication and authorization in SmartERP."""

    __tablename__ = "users"

    # Surrogate primary key for stable references across the application.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )

    # Foreign key to companies for multi-tenancy. Every user belongs to exactly one company.
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Unique employee code used for HR and payroll integration.
    employee_code: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, index=True
    )

    # Unique username for login authentication.
    username: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True
    )

    # Unique email address for communication and password recovery.
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )

    # User's legal name components for display and reporting.
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Mobile number for two-factor authentication and notifications.
    mobile: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Bcrypt hash of the user's password. Never store plain text passwords.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Organizational structure fields for role-based access control.
    department: Mapped[str | None] = mapped_column(String(100), nullable=True)
    designation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'USER'"))

    # Account status flags for security and lifecycle management.
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true"), index=True
    )
    is_locked: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )

    # Security tracking for account lockout after failed login attempts.
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer, nullable=False, server_default=text("0")
    )

    # Audit timestamps for security monitoring and compliance.
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    password_changed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Automatic timestamps managed by the database.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Future relationships to other modules (e.g., permissions, audit logs) should be added here.
