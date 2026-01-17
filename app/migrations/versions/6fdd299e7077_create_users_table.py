"""create_users_table

Revision ID: 6fdd299e7077
Revises:
Create Date: 2026-01-15 16:21:47.306000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6fdd299e7077"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )
    op.create_index("ix_email", "users", ["email"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("ix_email", table_name="users")
    op.drop_table("users")
