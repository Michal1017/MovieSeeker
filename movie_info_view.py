import flet as ft
import machine_learning_algorithms
import api_calls


class MovieInfoPage:
    def __init__(self, movie_info):
        self.movie_info = movie_info
        self.similar_movies_list = machine_learning_algorithms.recommend_similar_movies(
            movie_info["id"]
        )

    def on_movie_click(self, page, row, movie_id):
        movie_id.clear()
        movie_id.append(row["id"])
        self.movie_info = api_calls.get_specific_movie(movie_id[0])
        self.similar_movies_list = machine_learning_algorithms.recommend_similar_movies(
            self.movie_info["id"]
        )
        movie_info_page = page.views[-1]
        movie_info_page.controls.clear()
        movie_info_page.controls.extend(
            [
                ft.AppBar(
                    title=ft.Text(self.movie_info["title"], size=20),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                self.build_movie_info_page(page, movie_id),
            ]
        )
        page.update()

    def build_similar_movies_tab(self, page, movie_id):
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
                    on_click=lambda _, row=row: self.on_movie_click(
                        page, row, movie_id
                    ),
                )
            )
        return elements

    def build_movie_info_page(self, page, movie_id):
        description = ft.Column(
            [
                ft.Text(self.movie_info["title"], size=50, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Text(
                        str(round(self.movie_info["vote_average"], 2)) + "/10",
                        size=30,
                    ),
                    bgcolor=ft.colors.BLUE_700,
                    padding=ft.padding.all(10),
                    border_radius=10,
                    margin=10,
                ),
                ft.Row(
                    [ft.Text(g["name"], italic=True) for g in self.movie_info["genres"]]
                ),
                ft.Text(self.movie_info["overview"], width=600, size=18),
                ft.Text(
                    "Release year: " + self.movie_info["release_date"][0:4], size=20
                ),
                ft.Text(
                    "Run time: " + str(self.movie_info["runtime"]) + " min", size=20
                ),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        movie_info_result = ft.Row(
            [
                ft.Image(
                    src=self.movie_info["poster_path"],
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
                    [self.build_similar_movies_tab(page, movie_id)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

    def build(self, page, movie_id):
        return ft.View(
            route="/movieInfo",
            controls=[
                ft.AppBar(
                    title=ft.Text(self.movie_info["title"], size=20),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                ),
                self.build_movie_info_page(page, movie_id),
            ],
        )
