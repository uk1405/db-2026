import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Row(ft.Text('안녕하세요'))
    )

ft.run(main)