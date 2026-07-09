"""Declarative base for SmartERP database models.

No models are defined here yet, but Alembic will import this module to
discover metadata when migrations are generated.
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


# Use a naming convention so future Alembic migrations remain deterministic.
NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)