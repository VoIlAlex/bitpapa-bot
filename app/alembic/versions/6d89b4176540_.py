"""empty message

Revision ID: 6d89b4176540
Revises: eb2601486e0f
Create Date: 2023-04-20 10:42:02.360469

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d89b4176540'
down_revision = 'eb2601486e0f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        table_name="offers",
        column_name="current_price_total_duration",
        type_=sa.BigInteger()
    )
    op.alter_column(
        table_name="offers",
        column_name="current_min_price_last_response_duration",
        type_=sa.BigInteger()
    )
    op.alter_column(
        table_name="offers",
        column_name="current_min_price_total_duration",
        type_=sa.BigInteger()
    )


def downgrade() -> None:
    op.alter_column(
        table_name="offers",
        column_name="current_price_total_duration",
        type_=sa.Integer(),
    )
    op.alter_column(
        table_name="offers",
        column_name="current_min_price_last_response_duration",
        type_=sa.Integer()
    )
    op.alter_column(
        table_name="offers",
        column_name="current_min_price_total_duration",
        type_=sa.Integer()
    )
