"""create initial tables

Revision ID: 2e37fa78da95
Revises: 
Create Date: 2021-07-18 20:07:13.505169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "2e37fa78da95"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("display_name", sa.String),
        sa.Column("hashed_password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_superuser", sa.Boolean, default=False),
        sa.Column("is_verified", sa.Boolean, default=False),
    )

    op.create_table(
        "incidents",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String, index=True),
        sa.Column("status", sa.String, index=True),
        sa.Column("description", sa.String, index=True),
        sa.Column("owner_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.ForeignKeyConstraint(
            ("owner_id",),
            ["users.id"],
        ),
    )


def downgrade():
    op.drop_table("incidents")
    op.drop_table("users")
