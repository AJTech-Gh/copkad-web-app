"""Rallies and Conv

Revision ID: 48dbe087b4d2
Revises: ebd69a83e5f7
Create Date: 2020-08-13 16:57:38.134586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48dbe087b4d2'
down_revision = 'ebd69a83e5f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rallies_and_conventions',
    sa.Column('cr_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('cr_type', sa.String(length=30), nullable=False),
    sa.Column('start_date_time', sa.DateTime(), nullable=False),
    sa.Column('end_date_time', sa.DateTime(), nullable=False),
    sa.Column('assembly', sa.String(length=30), nullable=False),
    sa.Column('venue', sa.String(length=50), nullable=False),
    sa.Column('souls_won', sa.Integer(), nullable=False),
    sa.Column('head_count', sa.Integer(), nullable=False),
    sa.Column('mode_of_count', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('cr_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rallies_and_conventions')
    # ### end Alembic commands ###
