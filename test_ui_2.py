import flet as ft

def main(page: ft.Page):
    page.title = "NBA Roster & Contract DBMS - 화면 2"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 650

    mock_players = [
        {"no": "23", "name": "르브론 제임스", "pos": "F", "ppg": "25.7", "salary": "$47.6M"},
        {"no": "3", "name": "앤서니 데이비스", "pos": "C", "ppg": "24.5", "salary": "$43.2M"},
        {"no": "0", "name": "윤동욱 (Rookie)", "pos": "G", "ppg": "28.1", "salary": "$12.5M"}
    ]

    table_rows = []
    for p in mock_players:
        table_rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(p["pos"])),
            ft.DataCell(ft.Text(p["no"])),
            ft.DataCell(ft.Text(p["name"], weight="bold")),
            ft.DataCell(ft.Text(p["ppg"], color="amber")),
            ft.DataCell(ft.Text(p["salary"], color="greenaccent")),
        ]))

    page.add(ft.Column([
        ft.Container(ft.Text("📋 2. 소속 계약 선수 로스터", size=18, weight="bold", color="orangeaccent"), padding=5),
        ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("포지션")),
                    ft.DataColumn(ft.Text("번호")),
                    ft.DataColumn(ft.Text("이름")),
                    ft.DataColumn(ft.Text("PPG")),
                    ft.DataColumn(ft.Text("연봉")),
                ],
                rows=table_rows,
                heading_row_color="black38",
                column_spacing=12
            ),
            bgcolor="black26", border_radius=12, padding=5
        )
    ], spacing=10, horizontal_alignment="center"))

ft.app(target=main)
