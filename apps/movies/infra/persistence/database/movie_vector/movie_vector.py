from uuid import UUID

from sqlalchemy import Column, TEXT
from sqlalchemy.orm import Mapped, mapped_column

from apps.shared.infra.persistence.database.base import Base


class MovieVectorRow(Base):
    __tablename__ = "movie_vector"
    movie_id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    vector = Column(TEXT, nullable=False)
