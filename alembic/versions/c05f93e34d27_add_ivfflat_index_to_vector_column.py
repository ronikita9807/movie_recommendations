"""Add ivfflat index to vector column

Revision ID: c05f93e34d27
Revises: 9c6bdcd74f4g
Create Date: 2024-11-26 01:58:57.774009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c05f93e34d27'
down_revision = '9c6bdcd74f4g'
branch_labels = None
depends_on = None


def upgrade():
    # Создаем индекс ivfflat для колонки vector
    op.execute("""
        CREATE INDEX movie_vector_idx 
        ON movie_vector 
        USING ivfflat (vector) 
        WITH (lists = 100);
    """)


def downgrade():
    # Удаляем индекс
    op.execute("DROP INDEX IF EXISTS movie_vector_idx")
