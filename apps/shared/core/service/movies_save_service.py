from pathlib import Path


from apps.movies.core.ports.requires.movies_repo import MoviesRepository

from apps.shared.core.service.data_service import MoviesDataService

DATA_DIR = Path(__file__).resolve().parent


class MoviesSaveService:
    def __init__(
        self,
        movies_repo: MoviesRepository,
        movies_data_service: MoviesDataService,
    ):
        self._movies_data_service = movies_data_service
        self._movies_repo = movies_repo

    def update_movies(self) -> None:
        movies = self._movies_data_service.get_movies_data()
        self._movies_repo.save(movies)

    def delete_movies(self) -> None:
        return self._movies_repo.delete()
