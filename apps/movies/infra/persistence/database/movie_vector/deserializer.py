from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.infra.persistence.database.movie_vector.movie_vector import (
    MovieVectorRow,
)


def deserialize_movie_vector(movie_vector_row: MovieVectorRow) -> MovieVector:
    return MovieVector(
        vector=movie_vector_row.vector,
        movie_id=movie_vector_row.movie_id,
    )
