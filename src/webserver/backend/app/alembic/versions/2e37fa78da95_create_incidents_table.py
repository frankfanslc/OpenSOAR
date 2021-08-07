"""create incidents and users table

Revision ID: 2e37fa78da95
Revises: 
Create Date: 2021-07-18 20:07:13.505169

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2e37fa78da95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
    )
    op.create_table(
        'incidents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, index=True),
        sa.Column('description', sa.String, index=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'))
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('incidents')

