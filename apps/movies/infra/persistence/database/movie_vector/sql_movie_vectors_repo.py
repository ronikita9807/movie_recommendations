from typing import Optional
from uuid import UUID

from sqlalchemy import text
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


# Сделать протокол репозитория в отдельном файле
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

    def get_movies_by_embeddings(
        self, vector: list[float], limit: int = 10
    ) -> list[UUID]:
        query_vector = "[" + ", ".join(map(str, vector)) + "]"

        query = text("""
                    SELECT movie_id, vector <=> CAST(:query_vector AS vector) AS distance
                    FROM movie_vector
                    ORDER BY distance ASC
                    LIMIT :limit
                """)
        result = self.session.execute(
            query, {"query_vector": query_vector, "limit": limit}
        )
        return [row.movie_id for row in result]

    # переписать репозитории
    def save(self, movie_vectors: list[MovieVector]) -> None:
        movie_vectors_row = [
            serialize_movie_vector(movie_vector) for movie_vector in movie_vectors
        ]
        self.session.add_all(movie_vectors_row)
        self.session.commit()

    def delete(self):
        self.session.query(MovieVectorRow).delete()
        self.session.commit()
