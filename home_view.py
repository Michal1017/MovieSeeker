import flet as ft
import api_calls


class HomeView:
    def __init__(self):
        self.most_popular_movies_list = api_calls.GetMostPopularMoviesList()
        self.title = "MovieSeeker"

    def on_button_search_click(self, page, movieTitleInput, movieTitle):
        movieTitle.clear()
        movieTitle.append(movieTitleInput.value)
        page.go("/foundMovies")

    def build_search_tab(self, page, movieTitle):
        searchTextField = ft.TextField(
            label="Movie title",
            hint_text="Please, enter movie title",
            width=600,
            border_color=ft.colors.BLUE_100,
        )

        sumbitButton = ft.ElevatedButton(
            text="Search",
            icon="search",
            on_click=lambda _: self.on_button_search_click(
                page, searchTextField, movieTitle
            ),
        )

        return ft.Row(
            [searchTextField, sumbitButton],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def on_movie_click(self, page, row, movieId):
        movieId.clear()
        movieId.append(row["id"])
        page.go("/movieInfo")

    def build_most_popular_movies_tab(self, page, movieId):
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
                    on_click=lambda _, row=row: self.on_movie_click(page, row, movieId),
                )
            )

        return ft.Column(
            [
                ft.Text("Most Popular Movies", size=30, color=ft.colors.BLUE_200),
                elements,
            ],
            width=1160,
            height=340,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def build(self, page, movieTitle, movieId):
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
                        self.build_search_tab(page, movieTitle),
                        ft.Row(
                            [self.build_most_popular_movies_tab(page, movieId)],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                )
            ],
        )
