import flet as ft
import API_calls
import Most_Popular_Films_Tab as MPFT

mostPopularFilmsTab = MPFT.MostPopularFilmsTab()

def main(page: ft.Page):
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

    page.add(ft.Column(
                [
                    ft.Row(
                        [title],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [mostPopularFilmsTab.build()],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                expand=True)
            )

    page.update()


ft.app(target=main)