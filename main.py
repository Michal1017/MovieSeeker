import flet as ft
import api_calls
import home_view
import movie_info_view
import search_result_view


def main(page: ft.Page):
    movieId = []
    movieTitle = []
    page.title = "MovieSeeker"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    homeView = home_view.HomeView()

    def route_change(route):
        page.views.clear()
        page.views.append(homeView.build(page, movieTitle, movieId))
        if page.route == "/movieInfo":
            movieInfo = api_calls.GetSpecificMovie(movieId[0])
            movie_info_view_object = movie_info_view.MovieInfoPage(movieInfo)
            page.views.append(movie_info_view_object.build(page, movieId))
        if page.route == "/foundMovies":
            movieList = api_calls.MovieListByTitle(movieTitle[0])
            search_result_view_object = search_result_view.SearchResultView(movieList)
            page.views.append(search_result_view_object.build(page, movieId))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
