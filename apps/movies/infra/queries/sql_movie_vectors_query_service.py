from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from apps.movies.core.ports.queries.movie_vectors_query_service import MovieVectorsQueryService


class PostgreSQLMovieVectorsQueryService(MovieVectorsQueryService):
    def __init__(self, session: Session):
        self.session = session

    def get_movies_by_embeddings(self, vector: list[float], limit: int = 10) -> list[UUID]:
        query_vector = "[" + ", ".join(map(str, vector)) + "]"
        stmt = text(
            """
            SELECT movie_id
            FROM movie_vector
            ORDER BY vector <=> CAST(:query_vector AS vector)
            LIMIT :limit
            """
        )
        with self.session.begin():
            result = self.session.execute(
                stmt, {"query_vector": query_vector, "limit": limit}
            )
            movie_ids = [row.movie_id for row in result]
        return movie_ids
