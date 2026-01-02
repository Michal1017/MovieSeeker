import flet as ft


class SearchResultView:
    def __init__(self, movie_list):
        self.title = "Search Result"
        self.movie_list = movie_list

    def on_movie_click(self, page, row, movie_id):
        movie_id.clear()
        movie_id.append(row["id"])
        page.go("/movieInfo")

    def build(self, page, movie_id):
        if self.movie_list.empty:
            return ft.View(
                route="/foundMovies",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Results", size=20),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                    ),
                    ft.Text("No results"),
                ],
            )
        else:
            elements = ft.Column(expand=1, scroll=ft.ScrollMode.AUTO, spacing=10)
            elements.controls.clear()
            for _, row in self.movie_list.iterrows():
                elements.controls.append(
                    ft.TextButton(
                        content=ft.Row(
                            [
                                ft.Image(
                                    src=row["poster_path"],
                                    width=100,
                                    height=100,
                                    fit=ft.ImageFit.FILL,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                    border_radius=ft.border_radius.all(10),
                                ),
                                ft.Text(
                                    row["title"],
                                    size=18,
                                    color=ft.colors.BLUE_100,
                                    weight=ft.FontWeight.BOLD,
                                    width=600,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(row["release_date"], size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        tooltip=row["title"],
                        on_click=lambda _, row=row: self.on_movie_click(
                            page, row, movie_id
                        ),
                    )
                )

            search_result = ft.Column(
                [ft.Text(self.title, size=30, color=ft.colors.BLUE_200), elements],
                width=1160,
                height=600,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

            return ft.View(
                route="/foundMovies",
                controls=[
                    ft.AppBar(
                        title=ft.Text("Results", size=20),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                    ),
                    search_result,
                ],
            )
