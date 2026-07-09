"""create companies table

Revision ID: 20240628_create_companies_table
Revises: 
Create Date: 2026-06-28 11:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20240628_create_companies_table'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the companies table with all columns, indexes, and constraints."""
    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('company_code', sa.String(length=32), nullable=False),
        sa.Column('company_name', sa.String(length=255), nullable=False),
        sa.Column('legal_name', sa.String(length=255), nullable=False),
        sa.Column('gst_number', sa.String(length=20), nullable=True),
        sa.Column('pan_number', sa.String(length=10), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('phone', sa.String(length=32), nullable=True),
        sa.Column('mobile', sa.String(length=32), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('address_line1', sa.String(length=255), nullable=True),
        sa.Column('address_line2', sa.String(length=255), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('country', sa.String(length=100), nullable=True),
        sa.Column('pincode', sa.String(length=20), nullable=True),
        sa.Column('financial_year_start', sa.Date(), nullable=True),
        sa.Column('financial_year_end', sa.Date(), nullable=True),
        sa.Column('currency', sa.String(length=3), server_default=sa.text("'INR'"), nullable=False),
        sa.Column('timezone', sa.String(length=64), server_default=sa.text("'Asia/Kolkata'"), nullable=False),
        sa.Column('logo', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_companies'),
        sa.UniqueConstraint('company_code', name='uq_companies_company_code')
    )
    op.create_index(op.f('ix_companies_city'), 'companies', ['city'], unique=False)
    op.create_index(op.f('ix_companies_gst_number'), 'companies', ['gst_number'], unique=False)
    op.create_index(op.f('ix_companies_is_active'), 'companies', ['is_active'], unique=False)
    op.create_index(op.f('ix_companies_pan_number'), 'companies', ['pan_number'], unique=False)
    op.create_index(op.f('ix_companies_state'), 'companies', ['state'], unique=False)
    op.create_index(op.f('ix_companies_email'), 'companies', ['email'], unique=False)


def downgrade() -> None:
    """Drop the companies table and all its indexes."""
    op.drop_index(op.f('ix_companies_email'), table_name='companies')
    op.drop_index(op.f('ix_companies_state'), table_name='companies')
    op.drop_index(op.f('ix_companies_pan_number'), table_name='companies')
    op.drop_index(op.f('ix_companies_is_active'), table_name='companies')
    op.drop_index(op.f('ix_companies_gst_number'), table_name='companies')
    op.drop_index(op.f('ix_companies_city'), table_name='companies')
    op.drop_table('companies')
