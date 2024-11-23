from apps.movies.core.domain.movie import Movie
from apps.movies.infra.persistence.database.movie.movie import MovieRow


def serialize_movie(movie: Movie) -> MovieRow:
    return MovieRow(
        movie_id=movie.movie_id,
        release_year=movie.release_year,
        title=movie.title,
        origin=movie.origin,
        director=movie.director,
        cast=movie.cast,
        genre=movie.genre,
        wiki_page=movie.wiki_page,
        plot=movie.plot,
    )
