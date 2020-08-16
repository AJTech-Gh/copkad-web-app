"""Updated dedication

Revision ID: b3bef60125e7
Revises: 3f52521a8eb8
Create Date: 2020-08-13 22:53:34.674260

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3bef60125e7'
down_revision = '3f52521a8eb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dedication',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_father', sa.String(length=20), nullable=False),
    sa.Column('id_mother', sa.String(length=20), nullable=False),
    sa.Column('child_name', sa.String(length=50), nullable=False),
    sa.Column('child_dob', sa.DateTime(), nullable=False),
    sa.Column('dedication_date_time', sa.DateTime(), nullable=False),
    sa.Column('officiating_minister', sa.String(length=50), nullable=False),
    sa.Column('assembly', sa.String(length=30), nullable=False),
    sa.Column('place_of_ceremony', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['id_father'], ['user.member_id'], ),
    sa.ForeignKeyConstraint(['id_mother'], ['user.member_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dedication_child_name'), 'dedication', ['child_name'], unique=False)
    op.create_index(op.f('ix_dedication_id_father'), 'dedication', ['id_father'], unique=False)
    op.create_index(op.f('ix_dedication_id_mother'), 'dedication', ['id_mother'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dedication_id_mother'), table_name='dedication')
    op.drop_index(op.f('ix_dedication_id_father'), table_name='dedication')
    op.drop_index(op.f('ix_dedication_child_name'), table_name='dedication')
    op.drop_table('dedication')
    # ### end Alembic commands ###