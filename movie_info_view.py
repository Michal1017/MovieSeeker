import flet as ft
import machine_learning_algorithms
import api_calls


class MovieInfoPage:
    def __init__(self, movieInfo):
        self.movieInfo = movieInfo
        self.similar_movies_list = machine_learning_algorithms.RecommendSimilarMovies(
            movieInfo["id"]
        )

    def on_movie_click(self, page, row, movieId):
        movieId.clear()
        movieId.append(row["id"])
        movieInfo = api_calls.GetSpecificMovie(movieId[0])
        self.movieInfo = movieInfo
        self.similar_movies_list = machine_learning_algorithms.RecommendSimilarMovies(
            movieInfo["id"]
        )
        movieInfoPage = page.views[-1]
        movieInfoPage.controls.clear()
        movieInfoPage.controls.extend(
            [
                ft.AppBar(
                    title=ft.Text(movieInfo["title"], size=20),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                self.build_movie_info_page(page, movieId),
            ]
        )
        page.update()

    def build_similar_movies_tab(self, page, movieId):
        elements = ft.Row(expand=1, scroll=ft.ScrollMode.AUTO, spacing=10)
        for _, row in self.similar_movies_list.iterrows():
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
        return elements

    def build_movie_info_page(self, page, movieId):
        description = ft.Column(
            [
                ft.Text(self.movieInfo["title"], size=50, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        str(round(self.movieInfo["vote_average"], 2)) + "/10",
                        size=30,
                    ),
                    bgcolor=ft.colors.BLUE_700,
                    padding=ft.padding.all(10),
                    border_radius=10,
                    margin=10,
                ),
                ft.Row(
                    [ft.Text(g["name"], italic=True) for g in self.movieInfo["genres"]]
                ),
                ft.Text(self.movieInfo["overview"], width=600, size=18),
                ft.Text(
                    "Release year: " + self.movieInfo["release_date"][0:4], size=20
                ),
                ft.Text(
                    "Run time: " + str(self.movieInfo["runtime"]) + " min", size=20
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        movie_info_result = ft.Row(
            [
                ft.Image(
                    src=self.movieInfo["poster_path"],
                    width=400,
                    height=600,
                    border_radius=20,
                ),
                description,
            ],
            spacing=50,
        )

        return ft.Column(
            [
                movie_info_result,
                ft.Row(
                    [self.build_similar_movies_tab(page, movieId)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def build(self, page, movieId):
        return ft.View(
            route="/movieInfo",
            controls=[
                ft.AppBar(
                    title=ft.Text(self.movieInfo["title"], size=20),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                self.build_movie_info_page(page, movieId),
            ],
        )
