"""sync user relationships & notifications

Revision ID: e6daa7f6d875
Revises: e99d94414028
Create Date: 2025-08-10 12:06:19.658894
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'e6daa7f6d875'
down_revision: Union[str, Sequence[str], None] = 'e99d94414028'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    # corporate_user_rights_history indeksleri (idempotent)
    if dialect == "postgresql":
        op.execute("CREATE INDEX IF NOT EXISTS ix_corporate_rights_changed_by ON corporate_user_rights_history (changed_by_admin_id)")
        op.execute("CREATE INDEX IF NOT EXISTS ix_corporate_rights_user_id ON corporate_user_rights_history (user_id)")
    else:
        # Diğer veritabanlarında çakışma riski varsa try/except yerine standart create deneyin
        op.create_index('ix_corporate_rights_changed_by', 'corporate_user_rights_history', ['changed_by_admin_id'], unique=False)
        op.create_index('ix_corporate_rights_user_id', 'corporate_user_rights_history', ['user_id'], unique=False)

    # user_relationships.created_at ekle (mevcut satırlar için default, sonra default'u kaldır)
    insp = sa.inspect(bind)
    cols = [c['name'] for c in insp.get_columns('user_relationships')]
    if 'created_at' not in cols:
        op.add_column('user_relationships', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
        op.alter_column('user_relationships', 'created_at', server_default=None)

    # relationship_type NOT NULL
    op.alter_column('user_relationships', 'relationship_type',
                    existing_type=sa.VARCHAR(length=32),
                    nullable=False)

    # user_relationships indeksleri (idempotent)
    if dialect == "postgresql":
        op.execute("CREATE INDEX IF NOT EXISTS ix_user_relationships_related_user_id ON user_relationships (related_user_id)")
        op.execute("CREATE INDEX IF NOT EXISTS ix_user_relationships_user_id ON user_relationships (user_id)")
        op.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'uq_user_rel_type'
                ) THEN
                    ALTER TABLE user_relationships
                    ADD CONSTRAINT uq_user_rel_type
                    UNIQUE (user_id, related_user_id, relationship_type);
                END IF;
            END $$;
        """)
    else:
        op.create_index('ix_user_relationships_related_user_id', 'user_relationships', ['related_user_id'], unique=False)
        op.create_index('ix_user_relationships_user_id', 'user_relationships', ['user_id'], unique=False)
        op.create_unique_constraint('uq_user_rel_type', 'user_relationships', ['user_id', 'related_user_id', 'relationship_type'])

def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    # Unique constraint kaldır
    if dialect == "postgresql":
        op.execute("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'uq_user_rel_type'
                ) THEN
                    ALTER TABLE user_relationships
                    DROP CONSTRAINT uq_user_rel_type;
                END IF;
            END $$;
        """)
        op.execute("DROP INDEX IF EXISTS ix_user_relationships_user_id")
        op.execute("DROP INDEX IF EXISTS ix_user_relationships_related_user_id")
    else:
        op.drop_constraint('uq_user_rel_type', 'user_relationships', type_='unique')
        op.drop_index('ix_user_relationships_user_id', table_name='user_relationships')
        op.drop_index('ix_user_relationships_related_user_id', table_name='user_relationships')

    op.alter_column('user_relationships', 'relationship_type',
                    existing_type=sa.VARCHAR(length=32),
                    nullable=True)

    # created_at sütununu sadece varsa kaldır
    insp = sa.inspect(bind)
    cols = [c['name'] for c in insp.get_columns('user_relationships')]
    if 'created_at' in cols:
        op.drop_column('user_relationships', 'created_at')

    # corporate_user_rights_history indekslerini kaldır
    if dialect == "postgresql":
        op.execute("DROP INDEX IF EXISTS ix_corporate_rights_user_id")
        op.execute("DROP INDEX IF EXISTS ix_corporate_rights_changed_by")
    else:
        op.drop_index('ix_corporate_rights_user_id', table_name='corporate_user_rights_history')
        op.drop_index('ix_corporate_rights_changed_by', table_name='corporate_user_rights_history')
