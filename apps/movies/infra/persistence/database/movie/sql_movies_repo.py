from typing import Optional, Iterable
from uuid import UUID

from sqlalchemy.orm import Session

from apps.movies.core.domain.movie import Movie
from apps.movies.core.ports.requires.movies_repo import MoviesRepository
from apps.movies.infra.persistence.database.movie.deserializer import (
    deserialize_movie,
)
from apps.movies.infra.persistence.database.movie.movie import MovieRow
from apps.movies.infra.persistence.database.movie.serializer import serialize_movie


class PostgreSQLMoviesRepository(MoviesRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, movie_id: UUID) -> Optional[Movie]:
        movie = (
            self.session.query(MovieRow).filter(MovieRow.movie_id == movie_id).first()
        )
        return deserialize_movie(movie) if movie else None

    def get_all_movies(self, batch_size=100) -> Iterable[Movie]:
        query = self.session.query(MovieRow).execution_options(stream_results=True)

        for movie_row in query:
            yield deserialize_movie(movie_row)

    def save(self, movies: list[Movie]) -> None:
        movies_row = [serialize_movie(movie) for movie in movies]
        self.session.add_all(movies_row)
        self.session.commit()

    def delete(self):
        self.session.query(MovieRow).delete()
        self.session.commit()
