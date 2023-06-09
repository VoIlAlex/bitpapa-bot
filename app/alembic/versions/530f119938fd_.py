"""empty message

Revision ID: 530f119938fd
Revises: 6d89b4176540
Create Date: 2023-04-26 14:56:11.159098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '530f119938fd'
down_revision = '6d89b4176540'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trades',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('external_ad_id', sa.String(length=255), nullable=True),
    sa.Column('external_conversation_id', sa.String(length=255), nullable=True),
    sa.Column('contractor_id', sa.String(length=255), nullable=True),
    sa.Column('contractor_user_name', sa.String(length=255), nullable=True),
    sa.Column('amount', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('status', sa.String(length=127), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('cost', sa.DECIMAL(precision=12, scale=2), nullable=True),
    sa.Column('external_status', sa.String(length=127), nullable=True),
    sa.Column('external_created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('external_completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('external_cancelled_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('external_paid_confirmed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('external_escrow_expired_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('transaction_url', sa.String(length=512), nullable=True),
    sa.Column('transaction_txid', sa.String(length=512), nullable=True),
    sa.Column('is_first', sa.Boolean(), nullable=True),
    sa.Column('greeting_sent', sa.Boolean(), nullable=True),
    sa.Column('requisites_sent', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id')
    )
    op.create_index(op.f('ix_trades_id'), 'trades', ['id'], unique=False)
    op.create_table('trades_bills',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('site_id', sa.String(length=127), nullable=True),
    sa.Column('bill_id', sa.String(length=255), nullable=False),
    sa.Column('amount_currency', sa.String(length=16), nullable=False),
    sa.Column('amount_value', sa.String(length=127), nullable=False),
    sa.Column('status_value', sa.String(length=63), nullable=False),
    sa.Column('status_changed_date_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('customer_phone', sa.String(length=63), nullable=True),
    sa.Column('customer_email', sa.String(length=63), nullable=True),
    sa.Column('customer_account', sa.String(length=63), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.Column('creation_date_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('expiration_date_time', sa.DateTime(timezone=True), nullable=True),
    sa.Column('pay_url', sa.String(length=255), nullable=False),
    sa.Column('trade_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('trade_id')
    )
    op.create_index(op.f('ix_trades_bills_id'), 'trades_bills', ['id'], unique=False)
    op.create_table('trades_messages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('external_id', sa.String(length=255), nullable=True),
    sa.Column('external_user_id', sa.String(length=255), nullable=True),
    sa.Column('external_user_name', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), nullable=True),
    sa.Column('attachment_url', sa.String(length=512), nullable=True),
    sa.Column('attachment_content_type', sa.String(length=127), nullable=True),
    sa.Column('is_handled', sa.Boolean(), nullable=False),
    sa.Column('trade_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['trade_id'], ['trades.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_id')
    )
    op.create_index(op.f('ix_trades_messages_id'), 'trades_messages', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trades_messages_id'), table_name='trades_messages')
    op.drop_table('trades_messages')
    op.drop_index(op.f('ix_trades_bills_id'), table_name='trades_bills')
    op.drop_table('trades_bills')
    op.drop_index(op.f('ix_trades_id'), table_name='trades')
    op.drop_table('trades')
    # ### end Alembic commands ###
