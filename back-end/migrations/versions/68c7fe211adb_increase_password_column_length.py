"""Increase password column length

Revision ID: 68c7fe211adb
Revises: ff46817a94ae
Create Date: 2024-12-19 22:46:20.215812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68c7fe211adb'
down_revision = 'ff46817a94ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.String(length=255),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
