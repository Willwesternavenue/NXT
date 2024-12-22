"""Create admin table

Revision ID: f6e067a093f3
Revises: 
Create Date: 2024-12-19 18:28:34.189579

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6e067a093f3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # ### Create the admin table ###
    op.create_table('admin',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('password', sa.String(length=100), nullable=False),  # 初期は100に設定
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###

def downgrade():
    # ### Drop the admin table ###
    op.drop_table('admin')
    # ### end Alembic commands ###flask db upgrade
