import flet as ft
import api_calls
import pandas as pd


class HomeView:
    def __init__(self):
        self.most_popular_movies_list = api_calls.get_most_popular_movies_list()
        self.title = "MovieSeeker"

    def on_button_search_click(self, page, movie_title_input, movie_title):
        movie_title.clear()
        movie_title.append(movie_title_input.value)
        page.go("/foundMovies")

    def build_search_tab(self, page, movie_title):
        search_test_field = ft.TextField(
            label="Movie title",
            hint_text="Please, enter movie title",
            width=600,
            border_color=ft.colors.BLUE_100,
        )

        sumbit_button = ft.ElevatedButton(
            text="Search",
            icon="search",
            on_click=lambda _: self.on_button_search_click(
                page, search_test_field, movie_title
            ),
        )

        return ft.Row(
            [search_test_field, sumbit_button],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def on_movie_click(self, page, row, movie_id):
        movie_id.clear()
        movie_id.append(row["id"])
        page.go("/movieInfo")

    def build_most_popular_movies_tab(self, page, movie_id):
        elements = ft.Row(expand=1, scroll=ft.ScrollMode.AUTO, spacing=10)
        for _, row in self.most_popular_movies_list.iterrows():
            elements.controls.append(
                ft.TextButton(
                    content=ft.Column(
                        [
                            ft.Image(
                                src=row["poster_path"],
                                width=200,
                                height=200,
                                fit=ft.ImageFit.FILL,
                                repeat=ft.ImageRepeat.NO_REPEAT,
                                border_radius=ft.border_radius.all(10),
                            ),
                            ft.Text(
                                "Rating: " + str(round(row["vote_average"], 1)) + "/10",
                                size=14,
                            ),
                            ft.Text(
                                row["title"],
                                size=18,
                                color=ft.colors.BLUE_100,
                                weight=ft.FontWeight.BOLD,
                                width=200,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    tooltip=row["title"],
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=lambda _, row=row: self.on_movie_click(
                        page, row, movie_id
                    ),
                )
            )

        return ft.Column(
            [
                ft.Text(
                    "Most Popular Movies",
                    size=30,
                    color=ft.colors.BLUE_700,
                    weight=ft.FontWeight.BOLD,
                ),
                elements,
            ],
            width=1160,
            height=340,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def on_button_find_movie_click(
        self, page, movie_id, result_layout, from_year, to_year, min_time, max_time
    ):
        result_layout.content.controls.clear()
        selected_movie = api_calls.find_movie_with_filters(
            from_year, to_year, min_time, max_time
        )

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

    def build_find_movie_for_you_layout(self, page, movie_id):
        from_year = ft.TextField(
            label="Year",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        to_year = ft.TextField(
            label="Year",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        min_time = ft.TextField(
            label="Minimal number of minutes",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

        max_time = ft.TextField(
            label="Maximal number of minutes",
            keyboard_type=ft.KeyboardType.NUMBER,
        )

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
            border=ft.border.all(10, ft.colors.BLUE_700),
            border_radius=12,
            padding=10,
        )

        input_data_layout = ft.Column(
            [
                ft.Text(
                    "Choose Movie For You",
                    size=30,
                    color=ft.colors.BLUE_700,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text("Choose release year range", size=24, color=ft.colors.BLUE_200),
                ft.Row(
                    [
                        ft.Text("From", size=18, color=ft.colors.BLUE_200),
                        from_year,
                        ft.Text("To", size=18, color=ft.colors.BLUE_200),
                        to_year,
                    ]
                ),
                ft.Text("Choose runtime", size=24, color=ft.colors.BLUE_200),
                ft.Row(
                    [
                        ft.Text("From", size=18, color=ft.colors.BLUE_200),
                        min_time,
                        ft.Text("Minutes To", size=18, color=ft.colors.BLUE_200),
                        max_time,
                        ft.Text("Minutes", size=18, color=ft.colors.BLUE_200),
                    ]
                ),
                result_film,
                ft.ElevatedButton(
                    content=ft.Text("Find movie", size=40, color=ft.colors.BLUE_200),
                    width=500,
                    height=80,
                    on_click=lambda _: self.on_button_find_movie_click(
                        page,
                        movie_id,
                        result_film,
                        from_year,
                        to_year,
                        min_time,
                        max_time,
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
        )

        # result_layout = ft.Column(
        #     horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        # )

        # result_layout.controls.extend(
        #     [
        #         ft.ElevatedButton(
        #             text="Find movie",
        #             on_click=lambda _: self.on_button_find_movie_click(
        #                 page, result_layout, from_year, to_year
        #             ),
        #         ),
        #     ]
        # )

        return input_data_layout

    def build(self, page, movie_title, movie_id):
        return ft.View(
            route="/",
            controls=[
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    self.title,
                                    size=80,
                                    text_align=ft.TextAlign.CENTER,
                                    color=ft.colors.BLUE_700,
                                    weight=ft.FontWeight.BOLD,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        self.build_search_tab(page, movie_title),
                        ft.Row(
                            [self.build_most_popular_movies_tab(page, movie_id)],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [self.build_find_movie_for_you_layout(page, movie_id)],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                    spacing=50,
                    scroll=ft.ScrollMode.AUTO,
                )
            ],
        )
