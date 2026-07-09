"""Dependency injection providers for SmartERP.

This module provides dependency functions for FastAPI's Depends()
to inject services and repositories into route handlers.
"""

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.repositories.company_repository import CompanyRepository
from app.services.company_service import CompanyService


def get_company_repository(db: Session = Depends(get_db)) -> CompanyRepository:
    """Provide a CompanyRepository instance.

    Args:
        db: Database session injected by FastAPI.

    Returns:
        CompanyRepository instance with database session.
    """
    return CompanyRepository(db)


def get_company_service(
    repository: CompanyRepository = Depends(get_company_repository),
) -> CompanyService:
    """Provide a CompanyService instance.

    Args:
        repository: CompanyRepository instance injected by FastAPI.

    Returns:
        CompanyService instance with repository.
    """
    return CompanyService(repository)
