from apps.movies.core.domain.movie import Movie
from apps.movies.core.ports.dto.movie import MovieDTO
from apps.movies.infra.persistence.database.movie.movie import MovieRow


def deserialize_dto_movie(movie_row: MovieRow) -> MovieDTO:
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


def deserialize_movie(movie_row: MovieRow) -> Movie:
    return Movie(
        release_year=movie_row.release_year,
        title=movie_row.title,
        origin=movie_row.origin,
        director=movie_row.director,
        cast=movie_row.cast,
        genre=movie_row.genre,
        wiki_page=movie_row.wiki_page,
        plot=movie_row.plot,
        movie_id=movie_row.movie_id,
    )
