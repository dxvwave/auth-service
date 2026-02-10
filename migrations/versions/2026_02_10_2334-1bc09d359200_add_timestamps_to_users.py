"""add_timestamps_to_users

Revision ID: 1bc09d359200
Revises: c87402dfedf7
Create Date: 2026-02-10 23:34:49.638826

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1bc09d359200"
down_revision: Union[str, Sequence[str], None] = "c87402dfedf7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add created_at and updated_at columns to users table
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove timestamp columns
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
