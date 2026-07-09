"""Company API endpoints for SmartERP v1.

This module provides RESTful endpoints for company master data operations.
All business logic is delegated to the service layer.
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies import get_company_service
from app.exceptions import (
    BusinessRuleError,
    CompanyNotFoundError,
    DuplicateCompanyCodeError,
    DuplicateGSTError,
    InvalidCompanyDataError,
)
from app.schemas.company import (
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)
from app.services.company_service import CompanyService

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post(
    "",
    summary="Create a new company",
    description="Create a new company master record with validation for unique company code and GST number.",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    company_data: CompanyCreate,
    service: Annotated[CompanyService, Depends(get_company_service)],
) -> CompanyResponse:
    """Create a new company record.

    Args:
        company_data: Validated company creation data.
        service: Injected company service.

    Returns:
        Created company response with generated id and timestamps.

    Raises:
        HTTPException: If business rule validation fails.
    """
    try:
        company = service.create_company(company_data)
        return company
    except DuplicateCompanyCodeError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except DuplicateGSTError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except InvalidCompanyDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "",
    summary="List all companies",
    description="Retrieve a paginated list of companies sorted by company name.",
    response_model=CompanyListResponse,
    status_code=status.HTTP_200_OK,
)
def list_companies(
    service: Annotated[CompanyService, Depends(get_company_service)],
    skip: Annotated[int, Query(ge=0, description="Number of records to skip")] = 0,
    limit: Annotated[
        int, Query(ge=1, le=100, description="Maximum number of records to return")
    ] = 20,
) -> CompanyListResponse:
    """Retrieve a paginated list of companies.

    Args:
        skip: Number of records to skip (offset).
        limit: Maximum number of records to return.
        service: Injected company service.

    Returns:
        Paginated list of company responses.
    """
    companies = service.list_companies(skip=skip, limit=limit)
    total = len(companies)
    total_pages = (total + limit - 1) // limit if total > 0 else 0
    page = (skip // limit) + 1 if limit > 0 else 1

    return CompanyListResponse(
        items=companies,
        total=total,
        page=page,
        page_size=limit,
        total_pages=total_pages,
    )


@router.get(
    "/{company_id}",
    summary="Get company by ID",
    description="Retrieve a specific company by its unique identifier.",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
)
def get_company(
    company_id: UUID,
    service: Annotated[CompanyService, Depends(get_company_service)],
) -> CompanyResponse:
    """Retrieve a company by its ID.

    Args:
        company_id: UUID of the company to retrieve.
        service: Injected company service.

    Returns:
        Company response with full details.

    Raises:
        HTTPException: If company is not found.
    """
    try:
        return service.get_company(company_id)
    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/{company_id}",
    summary="Update a company",
    description="Update an existing company record. Only provided fields will be updated.",
    response_model=CompanyResponse,
    status_code=status.HTTP_200_OK,
)
def update_company(
    company_id: UUID,
    company_data: CompanyUpdate,
    service: Annotated[CompanyService, Depends(get_company_service)],
) -> CompanyResponse:
    """Update an existing company record.

    Args:
        company_id: UUID of the company to update.
        company_data: Validated company update data.
        service: Injected company service.

    Returns:
        Updated company response.

    Raises:
        HTTPException: If company is not found or validation fails.
    """
    try:
        return service.update_company(company_id, company_data)
    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except DuplicateCompanyCodeError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except DuplicateGSTError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except BusinessRuleError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete(
    "/{company_id}",
    summary="Soft delete a company",
    description="Soft delete a company by setting is_active to False. This is the default delete operation.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def soft_delete_company(
    company_id: UUID,
    service: Annotated[CompanyService, Depends(get_company_service)],
) -> None:
    """Soft delete a company by setting is_active to False.

    Args:
        company_id: UUID of the company to soft delete.
        service: Injected company service.

    Raises:
        HTTPException: If company is not found.
    """
    try:
        service.soft_delete_company(company_id)
    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{company_id}/hard",
    summary="Hard delete a company",
    description="Permanently delete a company record from the database. Reserved for Super Admin functionality. This operation cannot be undone.",
    status_code=status.HTTP_204_NO_CONTENT,
)
def hard_delete_company(
    company_id: UUID,
    service: Annotated[CompanyService, Depends(get_company_service)],
) -> None:
    """Permanently delete a company record.

    Reserved for Super Admin functionality. Use with extreme caution
    as this operation cannot be undone and may violate data integrity
    if the company has related records.

    Args:
        company_id: UUID of the company to permanently delete.
        service: Injected company service.

    Raises:
        HTTPException: If company is not found.
    """
    try:
        service.hard_delete_company(company_id)
    except CompanyNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
