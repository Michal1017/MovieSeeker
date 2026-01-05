from dataclasses import dataclass
import flet as ft


@dataclass
class MoviesFilters:
    from_year: ft.TextField | None = None
    to_year: ft.TextField | None = None
    min_time: ft.TextField | None = None
    max_time: ft.TextField | None = None
    genres: list | None = None
    min_rating: ft.TextField | None = None
    max_rating: ft.TextField | None = None
    unwanted_genres: list | None = None
