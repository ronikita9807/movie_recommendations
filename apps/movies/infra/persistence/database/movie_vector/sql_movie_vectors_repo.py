from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.core.ports.requires.movie_vectors_repo import MovieVectorsRepository
from apps.movies.infra.persistence.database.movie_vector.deserializer import (
    deserialize_movie_vector,
)
from apps.movies.infra.persistence.database.movie_vector.movie_vector import (
    MovieVectorRow,
)
from apps.movies.infra.persistence.database.movie_vector.serializer import (
    serialize_movie_vector,
)


class PostgreSQLMovieVectorsRepository(MovieVectorsRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, movie_id: UUID) -> Optional[MovieVector]:
        movie = (
            self.session.query(MovieVectorRow)
            .filter(MovieVectorRow.movie_id == movie_id)
            .first()
        )
        return deserialize_movie_vector(movie) if movie else None

    def save(self, movie_vectors: list[MovieVector]) -> None:
        movie_vectors_row = [
            serialize_movie_vector(movie_vector) for movie_vector in movie_vectors
        ]
        self.session.add_all(movie_vectors_row)
        self.session.commit()

    def delete(self):
        self.session.query(MovieVectorRow).delete()
        self.session.commit()
