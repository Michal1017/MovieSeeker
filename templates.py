import flet as ft

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

    def build(self):
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
                                    'Rating: '+str(row['vote_average'])+'/10',
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