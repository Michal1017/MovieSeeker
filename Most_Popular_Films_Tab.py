import flet as ft
import API_calls

class MostPopularFilmsTab():
    
    def __init__(self) -> None:
        self.mostPopularTitle = ft.Text("Most Popular Films", size=30, color=ft.colors.BLUE_200)
        self.mostPopularList = ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.AUTO, spacing=20)
        self.mostPopularFilms = API_calls.GetMostPopularFilmsList()

    def build(self):
        for i, row in self.mostPopularFilms.iterrows():
            self.mostPopularList.controls.append(
                ft.Column(
                    [
                        ft.Image(
                            src = row['poster_path'],
                            width = 200,
                            height = 200,
                            fit = ft.ImageFit.FILL,
                            repeat = ft.ImageRepeat.NO_REPEAT,
                            border_radius = ft.border_radius.all(10),
                        ),
                        ft.Text('Rating: '+str(row['vote_average'])+'/10', size=14),
                        ft.Text(
                            row["original_title"], 
                            size=18, 
                            color=ft.colors.BLUE_100, 
                            weight=ft.FontWeight.BOLD,
                            width=200,
                        ),
                    ]
                )
            )
        
        return ft.Column([self.mostPopularTitle, self.mostPopularList], width=1080, height=400, horizontal_alignment=ft.CrossAxisAlignment.CENTER)