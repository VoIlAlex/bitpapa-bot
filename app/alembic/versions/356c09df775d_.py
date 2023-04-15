"""empty message

Revision ID: 356c09df775d
Revises: d20093f58513
Create Date: 2023-04-15 12:59:58.099375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '356c09df775d'
down_revision = 'd20093f58513'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offers', sa.Column('is_initialized', sa.Boolean(), nullable=True))
    op.add_column('offers', sa.Column('init_error', sa.Text(), nullable=True))
    op.add_column('offers', sa.Column('is_active', sa.Boolean(), nullable=True))
    op.add_column('offers', sa.Column('currency_code', sa.String(length=255), nullable=True))
    op.add_column('offers', sa.Column('crypto_currency_code', sa.String(length=255), nullable=True))
    op.add_column('offers', sa.Column('current_price', sa.DECIMAL(precision=12, scale=2), nullable=True))
    op.add_column('offers', sa.Column('current_min_price', sa.DECIMAL(precision=12, scale=2), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offers', 'current_min_price')
    op.drop_column('offers', 'current_price')
    op.drop_column('offers', 'crypto_currency_code')
    op.drop_column('offers', 'currency_code')
    op.drop_column('offers', 'is_active')
    op.drop_column('offers', 'init_error')
    op.drop_column('offers', 'is_initialized')
    # ### end Alembic commands ###
