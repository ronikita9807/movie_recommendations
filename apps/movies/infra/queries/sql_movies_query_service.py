from typing import Iterable
from uuid import UUID

from sqlalchemy.orm import Session

from apps.movies.core.ports.dto.movie import MovieDTO, MovieShortDTO
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.movies.infra.persistence.database.movie.movie import MovieRow


class PostgreSQLMoviesQueryService(MoviesQueryService):
    def __init__(self, session: Session):
        self.session = session

    def get_movies_by_ids(self, movie_ids: list[UUID]) -> list[MovieDTO]:
        movies = (
            self.session.query(MovieRow).filter(MovieRow.movie_id.in_(movie_ids)).all()
        )
        return [self._deserialize_movie(movie) for movie in movies]

    def get_all_movies(self, batch_size: int) -> Iterable[MovieShortDTO]:
        query = self.session.query(MovieRow).execution_options(stream_results=True)

        for movie_row in query:
            yield self._deserialize_short_movie(movie_row)

    def find_by_name(self, name: str) -> list[MovieDTO]:
        return [
            self._deserialize_movie(movie)
            for movie in self.session.query(MovieRow)
            .filter(MovieRow.title.ilike(f"%{name}%"))
            .all()
        ]

    @staticmethod
    def _deserialize_movie(movie_row: MovieRow) -> MovieDTO:
        return MovieDTO(
            release_year=movie_row.release_year,
            title=movie_row.title,
            origin=movie_row.origin,
            director=movie_row.director,
            cast=movie_row.cast,
            genre=movie_row.genre,
            wiki_page=movie_row.wiki_page,
            plot=movie_row.plot,
        )

    @staticmethod
    def _deserialize_short_movie(movie_row: MovieRow) -> MovieShortDTO:
        return MovieShortDTO(
            movie_id=movie_row.movie_id,
            title=movie_row.title,
            plot=movie_row.plot,
        )
