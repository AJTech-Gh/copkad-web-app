"""Updated dedication

Revision ID: 9370387a7978
Revises: b273787326ea
Create Date: 2020-08-13 23:20:04.220177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9370387a7978'
down_revision = 'b273787326ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dedication',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('member_id_father', sa.String(length=20), nullable=False),
    sa.Column('member_id_mother', sa.String(length=20), nullable=False),
    sa.Column('child_name', sa.String(length=50), nullable=False),
    sa.Column('child_dob', sa.DateTime(), nullable=False),
    sa.Column('dedication_date_time', sa.DateTime(), nullable=False),
    sa.Column('officiating_minister', sa.String(length=50), nullable=False),
    sa.Column('assembly', sa.String(length=30), nullable=False),
    sa.Column('place_of_ceremony', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dedication_child_name'), 'dedication', ['child_name'], unique=False)
    op.create_index(op.f('ix_dedication_member_id_father'), 'dedication', ['member_id_father'], unique=False)
    op.create_index(op.f('ix_dedication_member_id_mother'), 'dedication', ['member_id_mother'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dedication_member_id_mother'), table_name='dedication')
    op.drop_index(op.f('ix_dedication_member_id_father'), table_name='dedication')
    op.drop_index(op.f('ix_dedication_child_name'), table_name='dedication')
    op.drop_table('dedication')
    # ### end Alembic commands ###
