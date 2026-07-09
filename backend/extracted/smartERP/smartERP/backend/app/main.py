"""Application entrypoint for the SmartERP API.

This module keeps the FastAPI setup thin and delegates environment
configuration and route registration to focused modules.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


# Create the FastAPI application with explicit metadata for production use.
app = FastAPI(
	title=settings.app_name,
	version=settings.app_version,
	docs_url="/docs",
	redoc_url="/redoc",
	openapi_url="/openapi.json",
)


# Add CORS middleware early so all registered routes inherit the policy.
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_allow_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


# Register the API routes in a single place to keep the entrypoint minimal.
app.include_router(api_router)
