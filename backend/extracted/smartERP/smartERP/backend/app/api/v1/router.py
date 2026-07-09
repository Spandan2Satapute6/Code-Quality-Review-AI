"""Versioned API router for SmartERP."""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.company import router as company_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.root import router as root_router

# Centralized API Router
api_router = APIRouter()

# System Endpoints
api_router.include_router(root_router)
api_router.include_router(health_router)

# Authentication Endpoints
api_router.include_router(auth_router)

# Company Endpoints
api_router.include_router(company_router)