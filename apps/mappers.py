from apps.movies.infra.persistence.database.movie.movie import MovieRow
from apps.movies.infra.persistence.database.movie_vector.movie_vector import MovieVectorRow
from apps.shared.infra.persistence.database.base import Base


def init_all_mappers() -> list[type[Base]]:
    return [MovieRow, MovieVectorRow]
