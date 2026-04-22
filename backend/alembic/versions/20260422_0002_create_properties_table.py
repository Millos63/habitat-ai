"""create properties table

Revision ID: 20260422_0002
Revises: 20260422_0001
Create Date: 2026-04-22 00:30:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "20260422_0002"
down_revision: str | None = "20260422_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "properties",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=False, server_default="MXN"),
        sa.Column(
            "type",
            sa.Enum("house", "apartment", "land", "commercial", "office", name="property_type"),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.Enum("active", "paused", "sold", "rented", name="property_status"),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "operation",
            sa.Enum("sale", "rent", name="property_operation"),
            nullable=True,
        ),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("city", sa.String(length=255), nullable=True),
        sa.Column("state", sa.String(length=255), nullable=True),
        sa.Column("bedrooms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("bathrooms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("area_m2", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("images", postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["agent_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index("ix_properties_agent_id", "properties", ["agent_id"], unique=False)
    op.create_index("ix_properties_city", "properties", ["city"], unique=False)
    op.create_index("ix_properties_is_featured", "properties", ["is_featured"], unique=False)
    op.create_index("ix_properties_operation", "properties", ["operation"], unique=False)
    op.create_index("ix_properties_status", "properties", ["status"], unique=False)
    op.create_index("ix_properties_type", "properties", ["type"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_properties_type", table_name="properties")
    op.drop_index("ix_properties_status", table_name="properties")
    op.drop_index("ix_properties_operation", table_name="properties")
    op.drop_index("ix_properties_is_featured", table_name="properties")
    op.drop_index("ix_properties_city", table_name="properties")
    op.drop_index("ix_properties_agent_id", table_name="properties")
    op.drop_table("properties")

    op.execute("DROP TYPE IF EXISTS property_operation")
    op.execute("DROP TYPE IF EXISTS property_status")
    op.execute("DROP TYPE IF EXISTS property_type")
