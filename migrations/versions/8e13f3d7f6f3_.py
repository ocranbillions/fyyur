"""empty message

Revision ID: 8e13f3d7f6f3
Revises: 2fafc6bc3f51
Create Date: 2019-10-08 23:08:47.342784

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e13f3d7f6f3'
down_revision = '2fafc6bc3f51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_time', sa.DateTime(), nullable=True))
    op.drop_column('shows', 'start_date')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('start_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('shows', 'start_time')
    # ### end Alembic commands ###