from typing import Optional, Iterable
from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from apps.movies.core.domain.movie import Movie
from apps.movies.core.ports.requires.movies_repo import MoviesRepository
from apps.movies.infra.persistence.database.movie.deserializer import deserialize_movie
from apps.movies.infra.persistence.database.movie.movie import MovieRow
from apps.movies.infra.persistence.database.movie.serializer import serialize_movie


class PostgreSQLMoviesRepository(MoviesRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, movie_id: UUID) -> Optional[Movie]:
        stmt = select(MovieRow).where(MovieRow.movie_id == movie_id)
        with self.session.begin():
            movie_row = self.session.execute(stmt).scalar_one_or_none()
            return deserialize_movie(movie_row) if movie_row else None

    def get_all_movies(self, batch_size: int = 100) -> Iterable[Movie]:
        stmt = select(MovieRow).execution_options(stream_results=True)
        with self.session.begin():
            result = self.session.execute(stmt)
            for movie_row in result.scalars():
                yield deserialize_movie(movie_row)

    def save(self, movies: list[Movie]) -> None:
        rows = [serialize_movie(movie) for movie in movies]
        with self.session.begin():
            self.session.add_all(rows)

    def delete(self) -> None:
        stmt = delete(MovieRow)
        with self.session.begin():
            self.session.execute(stmt)