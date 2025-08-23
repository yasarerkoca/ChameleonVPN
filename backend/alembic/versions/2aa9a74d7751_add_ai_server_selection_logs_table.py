"""add ai_server_selection_logs table

Revision ID: 2aa9a74d7751
Revises: c4531481299d
Create Date: 2025-08-23 22:19:45.884142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2aa9a74d7751'
down_revision: Union[str, Sequence[str], None] = 'c4531481299d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ai_server_selection_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_ip', sa.String(length=64), nullable=False),
        sa.Column('selected_server_id', sa.Integer(), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('country', sa.String(length=64), nullable=True),
        sa.Column('reason', sa.String(length=256), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['selected_server_id'], ['vpn_servers.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ai_server_selection_logs_id'), 'ai_server_selection_logs', ['id'], unique=False)
    op.create_index(
        op.f('ix_ai_server_selection_logs_selected_server_id'),
        'ai_server_selection_logs',
        ['selected_server_id'],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        op.f('ix_ai_server_selection_logs_selected_server_id'),
        table_name='ai_server_selection_logs'
    )
    op.drop_index(op.f('ix_ai_server_selection_logs_id'), table_name='ai_server_selection_logs')
    op.drop_table('ai_server_selection_logs')
