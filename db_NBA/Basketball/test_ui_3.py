import flet as ft

def main(page: ft.Page):
    page.title = "NBA Roster & Contract DBMS - 화면 3"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 650

    page.add(ft.Column([
        ft.Container(ft.Text("✨ 3. 신규 유망주 분할 삽입 (CREATE)", size=18, weight="bold", color="orangeaccent"), padding=5),
        ft.TextField(label="선수 명 기입", hint_text="예: 윤동욱", width=360),
        ft.Dropdown(label="포지션 셀렉트", width=360, options=[ft.dropdown.Option("G"), ft.dropdown.Option("F"), ft.dropdown.Option("C")]),
        ft.TextField(label="계약 보장 연봉 ($)", value="950000", width=360),
        ft.ElevatedButton(
            content=ft.Text("로컬 인메모리 DB에 쓰기 확정", color="white", weight="bold"),
            bgcolor="green800", width=360, height=45
        )
    ], spacing=15, horizontal_alignment="center"))

ft.app(target=main)
