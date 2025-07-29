from typing import Optional
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.core.ports.requires.movie_vectors_repo import MovieVectorsRepository
from apps.movies.infra.persistence.database.movie_vector.deserializer import deserialize_movie_vector
from apps.movies.infra.persistence.database.movie_vector.movie_vector import MovieVectorRow
from apps.movies.infra.persistence.database.movie_vector.serializer import serialize_movie_vector


class PostgreSQLMovieVectorsRepository(MovieVectorsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, movie_id: UUID) -> Optional[MovieVector]:
        stmt = select(MovieVectorRow).where(
            MovieVectorRow.movie_id == movie_id
        )
        movie_row = self.session.execute(stmt).scalar_one_or_none()
        return deserialize_movie_vector(movie_row) if movie_row else None

    def save(self, movie_vectors: list[MovieVector]) -> None:
        rows = [serialize_movie_vector(mv) for mv in movie_vectors]
        with self.session.begin():
            self.session.add_all(rows)

    def delete(self) -> None:
        stmt = delete(MovieVectorRow)
        with self.session.begin():
            self.session.execute(stmt)