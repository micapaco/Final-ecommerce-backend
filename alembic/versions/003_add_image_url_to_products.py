"""Add image_url column to products table

Revision ID: 003_add_image_url
Revises: 002_add_client_id_to_bills
Create Date: 2026-02-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_image_url'
down_revision = '002_add_client_id'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add image_url column to products table."""
    op.add_column('products', sa.Column('image_url', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove image_url column from products table."""
    op.drop_column('products', 'image_url')
