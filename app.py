import flet as ft
import templates
import apicalls

mostPopularFilmsTab = templates.ScrollingTab(apicalls.GetMostPopularFilmsList(),
                                             "Most Popular Films")
searchTab = templates.SearchTab()


def main(page: ft.Page):
    movieId = []
    movieTitle = []
    page.title = "MovieSeeker"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.update()

    title = ft.Text(
            "MovieSeeker",
            size=80,
            text_align=ft.TextAlign.CENTER,
            color=ft.colors.BLUE_700, 
            weight=ft.FontWeight.BOLD
            )


    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.Column(
                    [
                        ft.Row(
                            [title],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        searchTab.build(page, movieTitle),
                        ft.Row(
                            [mostPopularFilmsTab.build(page, movieId)],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                expand=True,
                )
                ],
            )
        )
        if page.route == "/filmInfo":
            movieInfo=apicalls.GetSpecificMovie(movieId[0])
            movieInfoPage = templates.MovieInfoPage(movieInfo)
            page.views.append(
                ft.View(
                    "/filmInfo",
                    [
                        ft.AppBar(title=ft.Text(
                                            movieInfo['title'],
                                            size=20
                                        ),
                                            bgcolor=ft.colors.SURFACE_VARIANT
                        ),
                        movieInfoPage.build()
                    ],
                )
            )
        if page.route == "/foundMovies":
            movieList = apicalls.MovieListByTitle(movieTitle[0])
            if(movieList.empty):
                page.views.append(
                    ft.View(
                        "/foundMovies",
                        [
                            ft.AppBar(title=ft.Text(
                                                "Results",
                                                size=20
                                            ),
                                                bgcolor=ft.colors.SURFACE_VARIANT
                            ),
                            ft.Text('No results')
                        ],
                    )
                )
            else:
                searchResult = templates.SearchResult(movieList)
                page.views.append(
                    ft.View(
                        "/foundMovies",
                        [
                            ft.AppBar(title=ft.Text(
                                                "Results",
                                                size=20
                                            ),
                                                bgcolor=ft.colors.SURFACE_VARIANT
                            ),
                            searchResult.build(page, movieId)
                        ],
                    )
                )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)