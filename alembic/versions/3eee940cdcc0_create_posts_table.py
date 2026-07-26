"""create posts table

Revision ID: 3eee940cdcc0
Revises: 
Create Date: 2026-07-22 19:53:34.648309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3eee940cdcc0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column("title", sa.String(), nullable=False)
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("posts")
