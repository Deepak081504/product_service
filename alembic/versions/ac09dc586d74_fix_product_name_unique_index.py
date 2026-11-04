
"""fix product name unique index

Revision ID: ac09dc586d74
Revises: 985892f5627e
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ac09dc586d74"
down_revision: Union[str, Sequence[str], None] = "985892f5627e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(
        "ix_products_name_lower",
        table_name="products",
    )

    op.create_index(
        "ix_products_name_lower",
        "products",
        [sa.text("lower(name)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_products_name_lower",
        table_name="products",
    )
