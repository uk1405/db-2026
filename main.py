import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    # page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # def on_btn_click(e):
    #     # btn_change.content = '눌렸습니다'
    #     text_counter.value = '반갑습니다'
    #     page.update()

    # text_counter = ft.Text('안녕하세요')
    # btn_change = ft.Button('눌러 주세요', on_click=on_btn_click)

    text_counter = ft.Text(
        value='0',
        size=100,
        width=200,
        text_align=ft.TextAlign.CENTER,
    )

    def minus_click(e):
        text_counter.value = str(int(text_counter.value) - 1)

    def plus_click(e):
        text_counter.value = str(int(text_counter.value) + 1)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls = [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                text_counter,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ]
        )
    )

ft.run(main)