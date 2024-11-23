from typing import Optional, Iterable
from uuid import UUID

from sqlalchemy.orm import Session

from apps.movies.core.domain.movie import Movie
from apps.movies.core.ports.dto.movie import MovieDTO
from apps.movies.infra.persistence.database.movie.deserializer import (
    deserialize_movie,
    deserialize_dto_movie,
)
from apps.movies.infra.persistence.database.movie.movie import MovieRow
from apps.movies.infra.persistence.database.movie.serializer import serialize_movie


class PostgreSQLMovieRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, movie_id: UUID) -> Optional[Movie]:
        movie = self.session.query(MovieRow).filter(MovieRow.movie_id == movie_id).first()
        return deserialize_movie(movie) if movie else None

    def get_all_movies(self, batch_size=100) -> Iterable[Movie]:
        query = self.session.query(MovieRow)

        # Используем yield_per для ленивой загрузки данных по 100 штук
        # отваливается по таймауту так как транзакция закрывается, надо увеличить таймаут?
        for movie in query.yield_per(batch_size):
            yield deserialize_movie(movie)

    # вынести в query service
    def find_by_name(self, name: str) -> list[MovieDTO]:
        return [
            deserialize_dto_movie(movie)
            for movie in self.session.query(MovieRow)
            .filter(MovieRow.title.ilike(f"%{name}%"))
            .all()
        ]

    def save(self, movies: list[Movie]) -> None:
        movies_row = [serialize_movie(movie) for movie in movies]
        self.session.add_all(movies_row)
        self.session.commit()

    def delete(self):
        self.session.query(MovieRow).delete()
        self.session.commit()
