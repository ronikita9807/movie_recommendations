from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from apps.movies.core.ports.queries.movie_vectors_query_service import (
    MovieVectorsQueryService,
)


class PostgreSQLMovieVectorsQueryService(MovieVectorsQueryService):
    def __init__(self, session: Session):
        self.session = session

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
