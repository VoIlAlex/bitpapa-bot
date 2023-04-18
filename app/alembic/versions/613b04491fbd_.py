"""empty message

Revision ID: 613b04491fbd
Revises: 356c09df775d
Create Date: 2023-04-18 14:15:32.043017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '613b04491fbd'
down_revision = '356c09df775d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    UPDATE offers 
    SET is_initialized = FALSE, is_active = TRUE;
    """)
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('offers', 'is_initialized',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('offers', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('offers', 'is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('offers', 'is_initialized',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    # ### end Alembic commands ###
