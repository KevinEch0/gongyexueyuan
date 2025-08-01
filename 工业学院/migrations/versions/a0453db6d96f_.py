"""empty message

Revision ID: a0453db6d96f
Revises: edb1fee861f7
Create Date: 2025-07-10 09:44:57.245710

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0453db6d96f'
down_revision = 'edb1fee861f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('t_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('desc', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_role')
    # ### end Alembic commands ###
