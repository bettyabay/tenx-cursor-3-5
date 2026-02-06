"""Initial schema: trends and platform_connections

Revision ID: 001_initial
Revises: 
Create Date: 2026-02-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create platform_connections table
    op.create_table(
        'platform_connections',
        sa.Column('connection_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('platform_name', sa.Enum('TWITTER', 'TIKTOK', 'INSTAGRAM', name='platform'), nullable=False),
        sa.Column('connection_status', sa.Enum('CONNECTED', 'DISCONNECTED', 'RATE_LIMITED', name='connectionstatus'), nullable=False),
        sa.Column('rate_limit_status', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('last_sync_timestamp', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_error', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('connection_id'),
        sa.UniqueConstraint('platform_name', name='uq_platform_connection_platform_name')
    )
    
    # Create trends table
    op.create_table(
        'trends',
        sa.Column('trend_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('topic_name', sa.String(length=500), nullable=False),
        sa.Column('platform', sa.Enum('TWITTER', 'TIKTOK', 'INSTAGRAM', name='platform'), nullable=False),
        sa.Column('engagement_metrics', postgresql.JSON(astext_type=sa.Text()), nullable=False),
        sa.Column('trend_velocity', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('relevance_score', sa.Float(), nullable=True),
        sa.Column('related_hashtags', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('platform_trend_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('trend_id'),
        sa.CheckConstraint('relevance_score >= 0.0 AND relevance_score <= 1.0', name='check_relevance_score_range')
    )
    
    # Create indexes
    op.create_index('ix_trends_platform_timestamp', 'trends', ['platform', 'timestamp'])
    op.create_index('ix_trends_relevance_score', 'trends', ['relevance_score'])
    op.create_index('ix_trends_timestamp', 'trends', ['timestamp'])
    op.create_index('ix_platform_connections_platform_name', 'platform_connections', ['platform_name'])
    
    # Create unique constraint for trends
    op.create_unique_constraint('uq_trends_platform_trend_id_timestamp', 'trends', ['platform', 'platform_trend_id', 'timestamp'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_platform_connections_platform_name', table_name='platform_connections')
    op.drop_index('ix_trends_timestamp', table_name='trends')
    op.drop_index('ix_trends_relevance_score', table_name='trends')
    op.drop_index('ix_trends_platform_timestamp', table_name='trends')
    
    # Drop tables
    op.drop_table('trends')
    op.drop_table('platform_connections')
    
    # Drop enums
    sa.Enum(name='connectionstatus').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='platform').drop(op.get_bind(), checkfirst=True)
