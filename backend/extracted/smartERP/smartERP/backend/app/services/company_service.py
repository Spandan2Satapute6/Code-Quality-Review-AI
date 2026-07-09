"""Company service for business logic and orchestration.

This service layer contains all business rules for the Company entity.
It orchestrates repository calls and enforces business constraints.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from app.exceptions import (
    CompanyNotFoundError,
    DuplicateCompanyCodeError,
    DuplicateGSTError,
    InvalidCompanyDataError,
)
from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:
    """Service for Company entity business operations."""

    def __init__(self, repository: CompanyRepository) -> None:
        """Initialize service with injected repository."""
        self.repository = repository

    def create_company(self, company_data: CompanyCreate) -> Company:
        """Create a new company with business rule validation.

        Business rules:
        - Company code must be unique
        - GST number must be unique if provided
        - Company name cannot be empty after trimming

        Args:
            company_data: Validated company creation data from Pydantic schema.

        Returns:
            Created Company SQLAlchemy model instance.

        Raises:
            DuplicateCompanyCodeError: If company code already exists.
            DuplicateGSTError: If GST number already exists.
            InvalidCompanyDataError: If company name is empty after trimming.
        """
        # Check company code uniqueness
        if self.repository.exists_by_company_code(company_data.company_code):
            raise DuplicateCompanyCodeError(
                f"Company with code '{company_data.company_code}' already exists"
            )

        # Check GST uniqueness if provided
        if company_data.gst_number and self.repository.exists_by_gst(
            company_data.gst_number
        ):
            raise DuplicateGSTError(
                f"Company with GST number '{company_data.gst_number}' already exists"
            )

        # Validate company name is not empty after trimming
        if not company_data.company_name or not company_data.company_name.strip():
            raise InvalidCompanyDataError("Company name cannot be empty")

        # Create Company model instance from schema data
        company = Company(
            company_code=company_data.company_code,
            company_name=company_data.company_name.strip(),
            legal_name=company_data.legal_name.strip(),
            gst_number=company_data.gst_number,
            pan_number=company_data.pan_number,
            email=company_data.email,
            phone=company_data.phone,
            mobile=company_data.mobile,
            website=str(company_data.website) if company_data.website else None,
            address_line1=company_data.address_line1.strip()
            if company_data.address_line1
            else None,
            address_line2=company_data.address_line2.strip()
            if company_data.address_line2
            else None,
            city=company_data.city.strip() if company_data.city else None,
            state=company_data.state.strip() if company_data.state else None,
            country=company_data.country.strip() if company_data.country else None,
            pincode=company_data.pincode.strip() if company_data.pincode else None,
            financial_year_start=company_data.financial_year_start,
            financial_year_end=company_data.financial_year_end,
            currency=company_data.currency,
            timezone=company_data.timezone,
            logo=company_data.logo,
            is_active=company_data.is_active,
        )

        return self.repository.create(company)

    def update_company(
        self, company_id: UUID, company_data: CompanyUpdate
    ) -> Company:
        """Update an existing company with business rule validation.

        Business rules:
        - Company must exist
        - Company code must remain unique if changed
        - GST number must remain unique if changed

        Args:
            company_id: UUID of the company to update.
            company_data: Validated company update data from Pydantic schema.

        Returns:
            Updated Company SQLAlchemy model instance.

        Raises:
            CompanyNotFoundError: If company does not exist.
            DuplicateCompanyCodeError: If new company code already exists.
            DuplicateGSTError: If new GST number already exists.
        """
        company = self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with id '{company_id}' not found")

        # Check company code uniqueness if being changed
        if company_data.company_code and company_data.company_code != company.company_code:
            if self.repository.exists_by_company_code(company_data.company_code):
                raise DuplicateCompanyCodeError(
                    f"Company with code '{company_data.company_code}' already exists"
                )
            company.company_code = company_data.company_code

        # Check GST uniqueness if being changed
        if company_data.gst_number and company_data.gst_number != company.gst_number:
            if self.repository.exists_by_gst(company_data.gst_number):
                raise DuplicateGSTError(
                    f"Company with GST number '{company_data.gst_number}' already exists"
                )
            company.gst_number = company_data.gst_number

        # Update fields if provided
        if company_data.company_name is not None:
            company.company_name = company_data.company_name.strip()
        if company_data.legal_name is not None:
            company.legal_name = company_data.legal_name.strip()
        if company_data.pan_number is not None:
            company.pan_number = company_data.pan_number
        if company_data.email is not None:
            company.email = company_data.email
        if company_data.phone is not None:
            company.phone = company_data.phone
        if company_data.mobile is not None:
            company.mobile = company_data.mobile
        if company_data.website is not None:
            company.website = str(company_data.website)
        if company_data.address_line1 is not None:
            company.address_line1 = company_data.address_line1.strip() or None
        if company_data.address_line2 is not None:
            company.address_line2 = company_data.address_line2.strip() or None
        if company_data.city is not None:
            company.city = company_data.city.strip() or None
        if company_data.state is not None:
            company.state = company_data.state.strip() or None
        if company_data.country is not None:
            company.country = company_data.country.strip() or None
        if company_data.pincode is not None:
            company.pincode = company_data.pincode.strip() or None
        if company_data.financial_year_start is not None:
            company.financial_year_start = company_data.financial_year_start
        if company_data.financial_year_end is not None:
            company.financial_year_end = company_data.financial_year_end
        if company_data.currency is not None:
            company.currency = company_data.currency
        if company_data.timezone is not None:
            company.timezone = company_data.timezone
        if company_data.logo is not None:
            company.logo = company_data.logo
        if company_data.is_active is not None:
            company.is_active = company_data.is_active

        return self.repository.update(company)

    def get_company(self, company_id: UUID) -> Company:
        """Retrieve a company by its ID.

        Args:
            company_id: UUID of the company to retrieve.

        Returns:
            Company SQLAlchemy model instance.

        Raises:
            CompanyNotFoundError: If company does not exist.
        """
        company = self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with id '{company_id}' not found")
        return company

    def get_company_by_code(self, company_code: str) -> Company:
        """Retrieve a company by its company code.

        Args:
            company_code: Unique company identifier.

        Returns:
            Company SQLAlchemy model instance.

        Raises:
            CompanyNotFoundError: If company does not exist.
        """
        company = self.repository.get_by_company_code(company_code)
        if not company:
            raise CompanyNotFoundError(
                f"Company with code '{company_code}' not found"
            )
        return company

    def list_companies(
        self, skip: int = 0, limit: int = 100
    ) -> list[Company]:
        """Retrieve a paginated list of companies.

        Args:
            skip: Number of records to skip (offset).
            limit: Maximum number of records to return.

        Returns:
            List of Company SQLAlchemy model instances sorted by company_name.
        """
        return self.repository.get_all(skip=skip, limit=limit)

    def soft_delete_company(self, company_id: UUID) -> Company:
        """Soft delete a company by setting is_active to False.

        This is the default delete operation for data integrity.

        Args:
            company_id: UUID of the company to soft delete.

        Returns:
            Updated Company SQLAlchemy model instance with is_active=False.

        Raises:
            CompanyNotFoundError: If company does not exist.
        """
        company = self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with id '{company_id}' not found")
        return self.repository.soft_delete(company)

    def hard_delete_company(self, company_id: UUID) -> None:
        """Permanently delete a company record from the database.

        Reserved for Super Admin functionality. Use with extreme caution
        as this operation cannot be undone and may violate data integrity
        if the company has related records.

        Args:
            company_id: UUID of the company to permanently delete.

        Raises:
            CompanyNotFoundError: If company does not exist.
        """
        company = self.repository.get_by_id(company_id)
        if not company:
            raise CompanyNotFoundError(f"Company with id '{company_id}' not found")
        self.repository.hard_delete(company)
