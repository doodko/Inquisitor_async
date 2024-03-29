"""Add statistics model

Revision ID: 1351c6cac101
Revises: 1c1cffbc9d56
Create Date: 2023-01-18 14:50:46.927445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1351c6cac101'
down_revision = '1c1cffbc9d56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statistics',
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('zone1_duration', sa.Interval(), nullable=False),
    sa.Column('zone2_duration', sa.Interval(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statistics')
    # ### end Alembic commands ###
