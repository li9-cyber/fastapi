"""add content column to posts table

Revision ID: dff736c8c7a2
Revises: 3eee940cdcc0
Create Date: 2026-07-22 23:41:41.589634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dff736c8c7a2'
down_revision: Union[str, Sequence[str], None] = '3eee940cdcc0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
