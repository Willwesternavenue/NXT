"""Increase password column length

Revision ID: ff46817a94ae
Revises: f6e067a093f3
Create Date: 2024-12-19 21:27:42.496739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff46817a94ae'
down_revision = 'f6e067a093f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### Increase password column length for 'users' table to 255 characters ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=100),  # existing column type
               type_=sa.String(length=255),  # change to VARCHAR(255)
               existing_nullable=False)

def downgrade():
    # ### Revert the password column length for 'users' table to 100 characters ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),  # existing column type
               type_=sa.String(length=100),  # revert to VARCHAR(100)
               existing_nullable=False)

