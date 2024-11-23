from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.infra.persistence.database.movie_vector.movie_vector import (
    MovieVectorRow,
)


def serialize_movie_vector(movie_vector: MovieVector) -> MovieVectorRow:
    return MovieVectorRow(
        movie_id=movie_vector.movie_id,
        vector=movie_vector.vector,
    )
