"""empty message

Revision ID: 35534c9ceb18
Revises: 477553bec210
Create Date: 2023-05-02 11:07:45.822625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35534c9ceb18'
down_revision = '477553bec210'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('offers', 'search_amount_limit_min')
    op.drop_column('offers', 'search_amount_limit_max')
    op.add_column('offers',
                  sa.Column('search_amount_limit_min', sa.DECIMAL(precision=12, scale=2), server_default='0.0',
                            nullable=False))
    op.add_column('offers',
                  sa.Column('search_amount_limit_max', sa.DECIMAL(precision=12, scale=2), server_default='0.0',
                            nullable=False))


def downgrade() -> None:
    op.drop_column('offers', 'search_amount_limit_min')
    op.drop_column('offers', 'search_amount_limit_max')
    op.add_column('offers',
                  sa.Column('search_amount_limit_min', sa.DECIMAL(precision=12, scale=8), server_default='0.0',
                            nullable=False))
    op.add_column('offers',
                  sa.Column('search_amount_limit_max', sa.DECIMAL(precision=12, scale=8), server_default='0.0',
                            nullable=False))
