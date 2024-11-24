from uuid import UUID

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from apps.shared.infra.persistence.database.base import Base


class MovieRow(Base):
    __tablename__ = "movie"

    movie_id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    release_year = Column(Integer)
    title = Column(String)
    origin = Column(String)
    director = Column(String)
    cast = Column(String)
    genre = Column(String)
    wiki_page = Column(String)
    plot = Column(String)
