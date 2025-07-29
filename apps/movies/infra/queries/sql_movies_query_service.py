from typing import Iterable
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.movies.core.ports.dto.movie import MovieDTO, MovieShortDTO
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.movies.infra.persistence.database.movie.movie import MovieRow


class PostgreSQLMoviesQueryService(MoviesQueryService):
    def __init__(self, session: Session):
        self.session = session

    def get_movies_by_ids(self, movie_ids: list[UUID]) -> list[MovieDTO]:
        stmt = select(MovieRow).where(MovieRow.movie_id.in_(movie_ids))
        with self.session.begin():
            results = self.session.execute(stmt).scalars().all()
        return [self._deserialize_movie(row) for row in results]

    def get_all_movies_by_batch(self, batch_size: int) -> Iterable[MovieShortDTO]:
        offset = 0
        while True:
            stmt = select(MovieRow).limit(batch_size).offset(offset)
            with self.session.begin():
                batch = self.session.execute(stmt).scalars().all()
            if not batch:
                break
            for row in batch:
                yield self._deserialize_short_movie(row)
            offset += batch_size

    def get_all_movies(self) -> Iterable[MovieShortDTO]:
        stmt = select(MovieRow)
        with self.session.begin():
            results = self.session.execute(stmt).scalars()
            for row in results:
                yield self._deserialize_short_movie(row)

    def find_by_name(self, name: str) -> list[MovieDTO]:
        pattern = f"%{name}%"
        stmt = select(MovieRow).where(MovieRow.title.ilike(pattern))
        with self.session.begin():
            results = self.session.execute(stmt).scalars().all()
        return [self._deserialize_movie(row) for row in results]

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