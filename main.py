import flet as ft
import api_calls
import home_view
import movie_info_view
import search_result_view


def main(page: ft.Page):
    movie_id = []
    movie_title = []
    page.title = "MovieSeeker"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    home_view_object = home_view.HomeView()

    def route_change(route):
        page.views.clear()
        page.views.append(home_view_object.build(page, movie_title, movie_id))
        if page.route == "/movieInfo":
            movieInfo = api_calls.get_specific_movie(movie_id[0])
            movie_info_view_object = movie_info_view.MovieInfoPage(movieInfo)
            page.views.append(movie_info_view_object.build(page, movie_id))
        if page.route == "/foundMovies":
            movie_list = api_calls.movie_list_by_title(movie_title[0])
            search_result_view_object = search_result_view.SearchResultView(movie_list)
            page.views.append(search_result_view_object.build(page, movie_id))
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)
