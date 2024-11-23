import csv
from pathlib import Path

from apps.movies.core.domain.movie import Movie


DATA_DIR = Path(__file__).resolve().parent


class MoviesDataService:
    def __init__(self):
        self._movies_data = self._init_data()

    def get_movies_data(self) -> list[Movie]:
        return self._movies_data

    @staticmethod
    def _init_data() -> list[Movie]:
        movies_data = []
        with open(DATA_DIR / "data/movies_dataset.csv", newline="\n") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for num, row in enumerate(spamreader):
                if num == 0:
                    continue
                movies_data.append(
                    Movie(
                        release_year=int(row[0]),
                        title=row[1],
                        origin=row[2],
                        director=row[3],
                        cast=row[4],
                        genre=row[5],
                        wiki_page=row[6],
                        plot=row[7],
                    )
                )
        return movies_data
