"""empty message

Revision ID: 20e1b0c588c9
Revises: 35534c9ceb18
Create Date: 2023-05-02 11:27:35.523193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20e1b0c588c9'
down_revision = '35534c9ceb18'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('offers', sa.Column('user_id', sa.String(length=255), nullable=True))
    op.add_column('offers', sa.Column('user_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('offers', 'user_name')
    op.drop_column('offers', 'user_id')
    # ### end Alembic commands ###