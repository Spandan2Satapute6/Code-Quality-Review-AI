"""Company master model for SmartERP.

This entity is the root of tenancy in the ERP. Every future business
module should reference ``company_id`` so records remain isolated per
company without requiring schema changes later.
"""

from __future__ import annotations

from datetime import date, datetime
import uuid

from sqlalchemy import Boolean, Date, DateTime, String, Text, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Company(Base):
    """Company master record used as the tenancy anchor for SmartERP."""

    __tablename__ = "companies"

    # Surrogate primary key for stable references across future ERP modules.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False,
    )

    # Short business identifier used in user-facing screens and imports.
    company_code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

    # Display name shown throughout the application.
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Registered legal name used for statutory and compliance documents.
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Compliance identifiers kept nullable because not every company is fully registered at onboarding.
    gst_number: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    pan_number: Mapped[str | None] = mapped_column(String(10), nullable=True, index=True)

    # Primary communication channels.
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(32), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Core address fields are kept flat to simplify reporting and future integrations.
    address_line1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # Financial year boundaries are stored as dates so reports can roll over cleanly.
    financial_year_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    financial_year_end: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Defaults are aligned with Indian ERP deployments.
    currency: Mapped[str] = mapped_column(String(3), nullable=False, server_default=text("'INR'"))
    timezone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        server_default=text("'Asia/Kolkata'"),
    )

    # Optional branding asset for printed documents and the UI shell.
    logo: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Soft activation flag for company lifecycle management.
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("true"), index=True
    )

    # Timestamps are managed automatically by the database.
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

    # Future company-scoped relations should be added here without changing the base schema.