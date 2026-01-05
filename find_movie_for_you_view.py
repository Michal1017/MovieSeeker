import flet as ft
import api_calls
import pandas as pd
from models.movies_filters import MoviesFilters


class FindMovieForYouView:
    def __init__(self):
        self.title = "Find Movie For You"

    def on_movie_click(self, page, row, movie_id):
        movie_id.clear()
        movie_id.append(row["id"])
        page.go("/movieInfo")

    def on_button_find_movie_click(self, page, movie_id, result_layout, movie_filters):

        result_layout.content.controls.clear()
        selected_movie = api_calls.find_movie_with_filters(movie_filters)

        if isinstance(selected_movie, str):
            result_layout.content.controls.extend(
                [
                    ft.Text(selected_movie, size=18, color=ft.colors.BLUE_200),
                ]
            )
        elif isinstance(selected_movie, pd.Series):
            result_layout.content.controls.extend(
                [
                    ft.TextButton(
                        content=ft.Column(
                            [
                                ft.Image(
                                    src=selected_movie["poster_path"],
                                    width=300,
                                    height=300,
                                    fit=ft.ImageFit.FILL,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                    border_radius=ft.border_radius.all(10),
                                ),
                                ft.Text(
                                    selected_movie["title"],
                                    size=18,
                                    color=ft.colors.BLUE_100,
                                    weight=ft.FontWeight.BOLD,
                                    width=200,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        tooltip=selected_movie["title"],
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20)
                        ),
                        on_click=lambda _: self.on_movie_click(
                            page, selected_movie, movie_id
                        ),
                    )
                ]
            )
        page.update()

    def build(self, page, movie_id):
        movie_filters = MoviesFilters()

        movie_filters.from_year = ft.TextField(
            label="Year",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        movie_filters.to_year = ft.TextField(
            label="Year",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        movie_filters.min_time = ft.TextField(
            label="Minimal number of minutes",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        movie_filters.max_time = ft.TextField(
            label="Maximal number of minutes",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        movie_filters.min_rating = ft.TextField(
            label="Minimal rating of movie",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        movie_filters.max_rating = ft.TextField(
            label="Maximal rating of movie",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        movie_filters.genres = []
        movie_filters.unwanted_genres = []

        list_of_genres = ft.Row(
            expand=1, scroll=ft.ScrollMode.AUTO, spacing=5, width=1000
        )
        list_of_unwanted_genres = ft.Row(
            expand=1, scroll=ft.ScrollMode.AUTO, spacing=5, width=1000
        )

        for genre in api_calls.get_movie_genres().values():
            checkbox = ft.Checkbox(label=genre)
            movie_filters.genres.append(checkbox)
            list_of_genres.controls.append(checkbox)
        for genre in api_calls.get_movie_genres().values():
            checkbox = ft.Checkbox(label=genre)
            movie_filters.unwanted_genres.append(checkbox)
            list_of_unwanted_genres.controls.append(checkbox)

        result_film = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(
                        name=ft.icons.QUESTION_MARK_ROUNDED,
                        size=200,
                        color=ft.colors.BLUE_700,
                    )
                ],
                width=300,
                height=400,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            alignment=ft.alignment.center,
            width=300,
            height=400,
            border=ft.border.all(10, ft.colors.BLUE_700),
            border_radius=12,
            padding=10,
        )

        input_data_layout = ft.Column(
            [
                ft.Text(
                    self.title,
                    size=80,
                    color=ft.colors.BLUE_700,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text("Choose release year range", size=24, color=ft.colors.BLUE_200),
                ft.Row(
                    [
                        ft.Text("From", size=18, color=ft.colors.BLUE_200),
                        movie_filters.from_year,
                        ft.Text("To", size=18, color=ft.colors.BLUE_200),
                        movie_filters.to_year,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text("Choose runtime", size=24, color=ft.colors.BLUE_200),
                ft.Row(
                    [
                        ft.Text("From", size=18, color=ft.colors.BLUE_200),
                        movie_filters.min_time,
                        ft.Text("Minutes To", size=18, color=ft.colors.BLUE_200),
                        movie_filters.max_time,
                        ft.Text("Minutes", size=18, color=ft.colors.BLUE_200),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    "Choose rating of movie between 0 and 10",
                    size=24,
                    color=ft.colors.BLUE_200,
                ),
                ft.Row(
                    [
                        ft.Text("From", size=18, color=ft.colors.BLUE_200),
                        movie_filters.min_rating,
                        ft.Text("Minutes To", size=18, color=ft.colors.BLUE_200),
                        movie_filters.max_rating,
                        ft.Text("Minutes", size=18, color=ft.colors.BLUE_200),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text("Choose genres you want", size=24, color=ft.colors.BLUE_200),
                list_of_genres,
                ft.Text(
                    "Choose genres you don't want", size=24, color=ft.colors.BLUE_200
                ),
                list_of_unwanted_genres,
                result_film,
                ft.ElevatedButton(
                    content=ft.Text("Find movie", size=40, color=ft.colors.BLUE_200),
                    width=500,
                    height=80,
                    on_click=lambda _: self.on_button_find_movie_click(
                        page, movie_id, result_film, movie_filters
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=25,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        return ft.View(
            route="/findMovieForYou",
            controls=[
                ft.AppBar(
                    title=ft.Text("Find Movie For You", size=20),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                input_data_layout,
            ],
        )
