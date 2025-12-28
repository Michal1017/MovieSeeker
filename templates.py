import flet as ft
import apicalls
import machine_learning_algorithms
# class which creates tab with actually most popular films
class ScrollingTab():
    
    def __init__(self, apiCall, title):
        self.title = ft.Text(
                            title,
                            size=30,
                            color=ft.colors.BLUE_200
                            )
        
        self.elements = ft.Row(
                           expand=1,
                           scroll=ft.ScrollMode.AUTO,
                           spacing=10
                          )
        
        self.filmList = apiCall

    def on_button_click(self, page, row, movieId):
        movieId.clear()
        movieId.append(row["id"])
        page.go("/filmInfo")

    def build(self, page, movieId):
        self.elements.controls.clear()
        for i, row in self.filmList.iterrows():
            self.elements.controls.append(
                ft.TextButton(
                    content=ft.Column(
                            [
                                ft.Image(
                                    src = row['poster_path'],
                                    width = 200,
                                    height = 200,
                                    fit = ft.ImageFit.FILL,
                                    repeat = ft.ImageRepeat.NO_REPEAT,
                                    border_radius = ft.border_radius.all(10),
                                ),
                                ft.Text(
                                    'Rating: '+str(round(row['vote_average'],1))+'/10',
                                    size=14
                                ),
                                ft.Text(
                                    row["title"], 
                                    size=18, 
                                    color=ft.colors.BLUE_100, 
                                    weight=ft.FontWeight.BOLD,
                                    width=200,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                    ),
                    tooltip=row["title"],
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=20)),
                    on_click=lambda _, row=row: self.on_button_click(page, row, movieId),
                )
            )
        
        result = ft.Column(
                    [
                        self.title,
                        self.elements
                    ],
                    width=1160,
                    height=340,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )

        return result
    
    # class which creates tab with information about specific movie
class MovieInfoPage():

    def __init__(self,movieInfo):
        self.title = ft.Text(
            movieInfo['title'],
            size=50,
            color=ft.colors.BLUE_100,
            weight=ft.FontWeight.BOLD,
        )
        self.genres = ft.Row()
        for genre in movieInfo['genres']:
            self.genres.controls.append(
                ft.Text(
                    genre['name'],
                    size=20,italic=True
                )
            )
        self.overview = ft.Text(
                            movieInfo['overview'],
                            size=18,
                            width=600
                        )
        self.poster_path = movieInfo['poster_path']
        self.release_date = ft.Text(
                                'Release year: ' + movieInfo['release_date'][0:4],
                                size=20
                            )
        self.runtime = ft.Text(
                            'Run time: ' + str(movieInfo['runtime']) + ' min',
                            size=20
                        )
        self.vote_average = ft.Container(
            content=ft.Text(
                        str(round(movieInfo['vote_average'],2)) + '/10',
                        size=30,
            ),
            bgcolor=ft.colors.BLUE_700,
            padding=ft.padding.all(10),
            border_radius=10,
            margin=10, 
        )

        self.similar_movies_title = ft.Text(
                                        "Similar movies",
                                        size=40
        )

        self.similarMoviesTab = ScrollingTab(machine_learning_algorithms.RecommendSimilarMovies(movieInfo['id']),
                                             "Similar Movies")

    def build(self, page, movieId):
        self.description = ft.Column(
            [
                self.title,
                self.vote_average,
                self.genres,
                self.overview,
                self.release_date,
                self.runtime,
            ],
            width=800,
            height=600,
            scroll=ft.ScrollMode.AUTO,
        )
        
        film_info = ft.Row([
            ft.Image(
                src = self.poster_path,
                width = 400,
                height = 600,
                fit = ft.ImageFit.FILL,
                repeat = ft.ImageRepeat.NO_REPEAT,
                border_radius = ft.border_radius.all(20),
            ),
            self.description,
        ],
        width= 1200,
        height= 600,
        spacing=50,
        )

        info_page = ft.Column(
                    [film_info,
                     self.similar_movies_title,
                     ft.Row(
                            [self.similarMoviesTab.build(page, movieId)],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )],
                     expand=True,
                     scroll=ft.ScrollMode.AUTO,
                     )

        return info_page

class SearchTab():
    def __init__(self, ):
        pass

    def on_button_click(self, page, movieTitleInput, movieTitle):
        movieTitle.clear()
        movieTitle.append(movieTitleInput.value)
        page.go("/foundMovies")

    def build(self, page, movieTitle):
        searchTextField = ft.TextField(label="Movie title",
                            hint_text="Please, enter movie title",
                            width=600,
                            border_color=ft.colors.BLUE_100
                )
        
        sumbitButton = ft.ElevatedButton(text="Search",
                                         icon="search",
                                         on_click=lambda _: self.on_button_click(page, searchTextField, movieTitle),
                            )

        result = ft.Row(
                            [searchTextField,
                             sumbitButton],
                            alignment=ft.MainAxisAlignment.CENTER,
                        )

        return result
    
class SearchResult():
    def __init__(self, movieList):
        self.title = ft.Text(
                            'Search Result',
                            size=30,
                            color=ft.colors.BLUE_200
                            )
        
        self.elements = ft.Column(
                           expand=1,
                           scroll=ft.ScrollMode.AUTO,
                           spacing=10
                          )
        
        self.movieList = movieList

    def on_button_click(self, page, row, movieId):
        movieId.clear()
        movieId.append(row["id"])
        page.go("/filmInfo")

    def build(self, page, movieId):
        self.elements.controls.clear()
        for i, row in self.movieList.iterrows():
            self.elements.controls.append(
                ft.TextButton(
                    content=ft.Row(
                            [
                                ft.Image(
                                    src = row['poster_path'],
                                    width = 100,
                                    height = 100,
                                    fit = ft.ImageFit.FILL,
                                    repeat = ft.ImageRepeat.NO_REPEAT,
                                    border_radius = ft.border_radius.all(10),
                                ),
                                ft.Text(
                                    row["title"], 
                                    size=18, 
                                    color=ft.colors.BLUE_100, 
                                    weight=ft.FontWeight.BOLD,
                                    width=600,
                                    overflow=ft.TextOverflow.ELLIPSIS
                                ),
                                ft.Text(
                                    row['release_date'],
                                    size=14
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                    ),
                    tooltip=row["title"],
                    on_click=lambda _, row=row: self.on_button_click(page, row, movieId),
                )
            )
        
        result = ft.Column(
                    [
                        self.title,
                        self.elements
                    ],
                    width=1160,
                    height=600,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )

        return result