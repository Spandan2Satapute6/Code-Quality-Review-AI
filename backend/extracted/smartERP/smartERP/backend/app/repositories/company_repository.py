"""Company repository for database operations.

This repository handles all database interactions for the Company entity.
It follows the Repository Pattern and contains no business logic or validation.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:
    """Repository for Company entity database operations."""

    def __init__(self, db: Session) -> None:
        """Initialize repository with database session."""
        self.db = db

    def create(self, company: Company) -> Company:
        """Create a new company record.

        Args:
            company: Company SQLAlchemy model instance to persist.

        Returns:
            The persisted Company instance with generated id and timestamps.
        """
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_by_id(self, company_id: UUID) -> Optional[Company]:
        """Retrieve a company by its primary key.

        Args:
            company_id: UUID of the company to retrieve.

        Returns:
            Company instance if found, None otherwise.
        """
        stmt = select(Company).where(Company.id == company_id)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_company_code(self, company_code: str) -> Optional[Company]:
        """Retrieve a company by its unique company code.

        Args:
            company_code: Unique company identifier.

        Returns:
            Company instance if found, None otherwise.
        """
        stmt = select(Company).where(Company.company_code == company_code)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_by_gst_number(self, gst_number: str) -> Optional[Company]:
        """Retrieve a company by GST number.

        Args:
            gst_number: GST identification number.

        Returns:
            Company instance if found, None otherwise.
        """
        stmt = select(Company).where(Company.gst_number == gst_number)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Company]:
        """Retrieve all companies with pagination support.

        Args:
            skip: Number of records to skip (offset).
            limit: Maximum number of records to return.

        Returns:
            List of Company instances sorted by company_name ascending.
        """
        stmt = (
            select(Company)
            .order_by(Company.company_name.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.execute(stmt).scalars().all())

    def update(self, company: Company) -> Company:
        """Update an existing company record.

        Args:
            company: Company SQLAlchemy model instance with updated fields.

        Returns:
            The updated Company instance.
        """
        self.db.commit()
        self.db.refresh(company)
        return company

    def soft_delete(self, company: Company) -> Company:
        """Soft delete a company by setting is_active to False.

        Args:
            company: Company SQLAlchemy model instance to soft delete.

        Returns:
            The updated Company instance with is_active set to False.
        """
        company.is_active = False
        company.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(company)
        return company

    def hard_delete(self, company: Company) -> None:
        """Permanently delete a company record from the database.

        Reserved for Super Admin functionality. Use with extreme caution
        as this operation cannot be undone and may violate data integrity
        if the company has related records.

        Args:
            company: Company SQLAlchemy model instance to delete permanently.
        """
        self.db.delete(company)
        self.db.commit()

    def exists_by_company_code(self, company_code: str) -> bool:
        """Check if a company with the given code exists.

        Args:
            company_code: Company code to check for existence.

        Returns:
            True if a company with the code exists, False otherwise.
        """
        stmt = select(Company).where(Company.company_code == company_code)
        return self.db.execute(stmt).scalar_one_or_none() is not None

    def exists_by_gst(self, gst_number: str) -> bool:
        """Check if a company with the given GST number exists.

        Args:
            gst_number: GST number to check for existence.

        Returns:
            True if a company with the GST number exists, False otherwise.
        """
        stmt = select(Company).where(Company.gst_number == gst_number)
        return self.db.execute(stmt).scalar_one_or_none() is not None
