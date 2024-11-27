from uuid import UUID

from sqlalchemy.orm import Session

from apps.movies.core.ports.dto.movie import MovieDTO
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.movies.infra.persistence.database.movie.deserializer import (
    deserialize_dto_movie,
)
from apps.movies.infra.persistence.database.movie.movie import MovieRow


class PostgreSQLMoviesQueryService(MoviesQueryService):
    def __init__(self, session: Session):
        self.session = session

    def get_movies_by_ids(self, movie_ids: list[UUID]) -> list[MovieDTO]:
        movies = (
            self.session.query(MovieRow).filter(MovieRow.movie_id.in_(movie_ids)).all()
        )
        return [deserialize_dto_movie(movie) for movie in movies]

    def find_by_name(self, name: str) -> list[MovieDTO]:
        return [
            deserialize_dto_movie(movie)
            for movie in self.session.query(MovieRow)
            .filter(MovieRow.title.ilike(f"%{name}%"))
            .all()
        ]
