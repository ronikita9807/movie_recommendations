"""chenge type column vector

Revision ID: 9c6bdcd74f4g
Revises: 9c6bdcd74f3c
Create Date: 2024-09-16 02:02:02.154828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import ARRAY

# revision identifiers, used by Alembic.
revision = "9c6bdcd74f4g"
down_revision = "9c6bdcd74f3c"
branch_labels = None
depends_on = None


def upgrade():
    # Добавляем расширение pgvector
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Изменяем тип колонки vector на VECTOR(300)
    op.execute("ALTER TABLE movie_vector ALTER COLUMN vector TYPE vector(300)")


def downgrade():
    # Возвращаем тип колонки vector обратно в ARRAY(Float)
    op.execute("ALTER TABLE movie_vector ALTER COLUMN vector TYPE FLOAT8[]")

    # Удаляем расширение pgvector
    op.execute("DROP EXTENSION IF EXISTS vector")
