"""add_timestamps_to_location_reviews

Revision ID: c2ecdcacc40d
Revises: 3d84cb99531b
Create Date: 2024-04-14 19:12:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2ecdcacc40d'
down_revision: str = '3d84cb99531b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('location_reviews', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))
    op.add_column('location_reviews', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('location_reviews', 'updated_at')
    op.drop_column('location_reviews', 'created_at') 