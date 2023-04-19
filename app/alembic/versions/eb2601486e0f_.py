"""empty message

Revision ID: eb2601486e0f
Revises: 3cb7214ee5fc
Create Date: 2023-04-19 16:27:42.173888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb2601486e0f'
down_revision = '3cb7214ee5fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column('offers', 'current_price_last_request_block')
    op.add_column('offers', sa.Column('current_price_last_request_block', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('offers', 'current_price_last_request_block')
    op.add_column('offers', sa.Column('current_price_last_request_block', sa.DateTime(timezone=True), nullable=True))
