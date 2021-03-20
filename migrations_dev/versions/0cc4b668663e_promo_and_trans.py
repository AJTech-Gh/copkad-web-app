"""promo and trans

Revision ID: 0cc4b668663e
Revises: 6d9f5e929157
Create Date: 2020-09-10 00:38:14.583942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cc4b668663e'
down_revision = '6d9f5e929157'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('promotion',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('member_id', sa.String(length=20), nullable=False),
    sa.Column('present_portfolio', sa.String(length=50), nullable=False),
    sa.Column('promoted_portfolio', sa.String(length=50), nullable=False),
    sa.Column('portfolio_specification', sa.String(length=80), nullable=False),
    sa.Column('promotion_date', sa.DateTime(), nullable=False),
    sa.Column('officiating_minister', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.member_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_promotion_member_id'), 'promotion', ['member_id'], unique=False)
    op.create_table('transfer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('member_id', sa.String(length=20), nullable=False),
    sa.Column('transformed_from', sa.String(length=50), nullable=False),
    sa.Column('transfered_to', sa.String(length=50), nullable=False),
    sa.Column('present_portfolio', sa.String(length=50), nullable=False),
    sa.Column('transfered_specification', sa.String(length=100), nullable=False),
    sa.Column('transfer_date', sa.DateTime(), nullable=False),
    sa.Column('officiating_minister', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['member_id'], ['user.member_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transfer_member_id'), 'transfer', ['member_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transfer_member_id'), table_name='transfer')
    op.drop_table('transfer')
    op.drop_index(op.f('ix_promotion_member_id'), table_name='promotion')
    op.drop_table('promotion')
    # ### end Alembic commands ###