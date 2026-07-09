"""Pydantic schemas for the SmartERP Company module.

These schemas are the API contract for company master data. They are
kept separate from the SQLAlchemy model so request and response shapes
can evolve without coupling to persistence details.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl, field_validator


GST_PATTERN = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[A-Z0-9]{3}$")
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$")
COMPANY_CODE_PATTERN = re.compile(r"^[A-Z0-9]{3,32}$")


class CompanyBase(BaseModel):
    """Common company fields shared by create, update, and response schemas."""

    company_code: str = Field(
        ...,
        min_length=3,
        max_length=32,
        description="Unique company identifier used across the ERP.",
        examples=["SMERP001"],
    )
    company_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Display name of the company.",
        examples=["SmartERP Trading Pvt Ltd"],
    )
    legal_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Registered legal name used on statutory documents.",
        examples=["SmartERP Trading Private Limited"],
    )
    gst_number: str | None = Field(
        default=None,
        max_length=15,
        description="Optional GST identification number in Indian format.",
        examples=["27AAPFU0939F1ZV"],
    )
    pan_number: str | None = Field(
        default=None,
        max_length=10,
        description="Optional PAN identification number in Indian format.",
        examples=["AAPFU0939F"],
    )
    email: EmailStr | None = Field(
        default=None,
        description="Primary contact email address.",
        examples=["accounts@smarterp.example"],
    )
    phone: str | None = Field(
        default=None,
        max_length=20,
        description="Landline or primary office phone number.",
        examples=["+91-22-40000000"],
    )
    mobile: str | None = Field(
        default=None,
        max_length=20,
        description="Primary mobile number.",
        examples=["+91-9876543210"],
    )
    website: HttpUrl | None = Field(
        default=None,
        description="Optional company website URL.",
        examples=["https://www.smarterp.example"],
    )
    address_line1: str | None = Field(
        default=None,
        max_length=255,
        description="First line of the company address.",
        examples=["123 Business Park"],
    )
    address_line2: str | None = Field(
        default=None,
        max_length=255,
        description="Second line of the company address.",
        examples=["Andheri East"],
    )
    city: str | None = Field(
        default=None,
        max_length=100,
        description="City where the company is registered or operated.",
        examples=["Mumbai"],
    )
    state: str | None = Field(
        default=None,
        max_length=100,
        description="State or region of the company address.",
        examples=["Maharashtra"],
    )
    country: str | None = Field(
        default=None,
        max_length=100,
        description="Country of operation.",
        examples=["India"],
    )
    pincode: str | None = Field(
        default=None,
        max_length=20,
        description="Postal or ZIP code.",
        examples=["400069"],
    )
    financial_year_start: date | None = Field(
        default=None,
        description="Start date of the financial year.",
        examples=["2026-04-01"],
    )
    financial_year_end: date | None = Field(
        default=None,
        description="End date of the financial year.",
        examples=["2027-03-31"],
    )
    currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
        description="Base accounting currency.",
        examples=["INR"],
    )
    timezone: str = Field(
        default="Asia/Kolkata",
        max_length=64,
        description="IANA timezone name used for timestamps and reports.",
        examples=["Asia/Kolkata"],
    )
    logo: str | None = Field(
        default=None,
        description="Optional logo reference or storage path.",
        examples=["https://cdn.example.com/logos/smarterp.png"],
    )
    is_active: bool = Field(
        default=True,
        description="Indicates whether the company is active in the ERP.",
        examples=[True],
    )

    @field_validator("company_code", mode="before")
    @classmethod
    def normalize_company_code(cls, value: Any) -> Any:
        """Normalize company codes to uppercase before validation."""

        if value is None:
            return value
        return str(value).strip().upper()

    @field_validator("company_code")
    @classmethod
    def validate_company_code(cls, value: str) -> str:
        """Ensure the company code is uppercase and within the allowed pattern."""

        if not COMPANY_CODE_PATTERN.fullmatch(value):
            raise ValueError("company_code must be uppercase alphanumeric and 3 to 32 characters long")
        return value

    @field_validator("gst_number")
    @classmethod
    def validate_gst_number(cls, value: str | None) -> str | None:
        """Validate the GST number format when provided."""

        if value is None:
            return value
        normalized = value.strip().upper()
        if not GST_PATTERN.fullmatch(normalized):
            raise ValueError("gst_number must match the Indian GST format")
        return normalized

    @field_validator("pan_number")
    @classmethod
    def validate_pan_number(cls, value: str | None) -> str | None:
        """Validate the PAN number format when provided."""

        if value is None:
            return value
        normalized = value.strip().upper()
        if not PAN_PATTERN.fullmatch(normalized):
            raise ValueError("pan_number must match the Indian PAN format")
        return normalized


class CompanyCreate(CompanyBase):
    """Schema used when creating a new company record."""


class CompanyUpdate(BaseModel):
    """Schema used for partial company updates."""

    model_config = ConfigDict(from_attributes=True)

    company_code: str | None = Field(
        default=None,
        min_length=3,
        max_length=32,
        description="Unique company identifier used across the ERP.",
        examples=["SMERP001"],
    )
    company_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Display name of the company.",
        examples=["SmartERP Trading Pvt Ltd"],
    )
    legal_name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        description="Registered legal name used on statutory documents.",
        examples=["SmartERP Trading Private Limited"],
    )
    gst_number: str | None = Field(default=None, max_length=15)
    pan_number: str | None = Field(default=None, max_length=10)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    mobile: str | None = Field(default=None, max_length=20)
    website: HttpUrl | None = None
    address_line1: str | None = Field(default=None, max_length=255)
    address_line2: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    country: str | None = Field(default=None, max_length=100)
    pincode: str | None = Field(default=None, max_length=20)
    financial_year_start: date | None = None
    financial_year_end: date | None = None
    currency: str | None = Field(default="INR", min_length=3, max_length=3)
    timezone: str | None = Field(default="Asia/Kolkata", max_length=64)
    logo: str | None = None
    is_active: bool | None = None

    @field_validator("company_code", mode="before")
    @classmethod
    def normalize_company_code(cls, value: Any) -> Any:
        if value is None:
            return value
        return str(value).strip().upper()

    @field_validator("company_code")
    @classmethod
    def validate_company_code(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not COMPANY_CODE_PATTERN.fullmatch(value):
            raise ValueError("company_code must be uppercase alphanumeric and 3 to 32 characters long")
        return value

    @field_validator("gst_number")
    @classmethod
    def validate_gst_number(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.strip().upper()
        if not GST_PATTERN.fullmatch(normalized):
            raise ValueError("gst_number must match the Indian GST format")
        return normalized

    @field_validator("pan_number")
    @classmethod
    def validate_pan_number(cls, value: str | None) -> str | None:
        if value is None:
            return value
        normalized = value.strip().upper()
        if not PAN_PATTERN.fullmatch(normalized):
            raise ValueError("pan_number must match the Indian PAN format")
        return normalized


class CompanyResponse(CompanyBase):
    """Schema returned after create, update, and fetch operations."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique company identifier.", examples=["550e8400-e29b-41d4-a716-446655440000"])
    created_at: datetime = Field(..., description="Record creation timestamp.")
    updated_at: datetime = Field(..., description="Record last update timestamp.")


class CompanyListResponse(BaseModel):
    """Paginated list response for company records."""

    model_config = ConfigDict(from_attributes=True)

    items: list[CompanyResponse] = Field(
        default_factory=list,
        description="List of company records for the current page.",
    )
    total: int = Field(
        default=0,
        ge=0,
        description="Total number of company records available.",
        examples=[1],
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Current page number.",
        examples=[1],
    )
    page_size: int = Field(
        default=20,
        ge=1,
        description="Number of items per page.",
        examples=[20],
    )
    total_pages: int = Field(
        default=0,
        ge=0,
        description="Total number of available pages.",
        examples=[1],
    )