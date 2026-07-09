"""
Database engine configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.config.settings import settings


engine: Engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
    pool_recycle=settings.database_pool_recycle,
    future=True,
)