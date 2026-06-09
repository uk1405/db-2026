import flet as ft

def main(page: ft.Page):
    page.title = "NBA Roster & Contract DBMS - 화면 4"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 650

    page.add(ft.Column([
        ft.Container(ft.Text("📊 4. 실시간 연산 보정 및 복합 Join", size=18, weight="bold", color="orangeaccent"), padding=5),
        ft.Container(
            content=ft.Column([
                ft.Text("📈 샐러리캡 및 연산 보정 지표", size=14, weight="bold", color="grey300"),
                ft.Divider(color="grey700"),
                ft.Text("팀 샐러리캡 총합산 (SUM 연산):", size=12),
                ft.Text("$103,300,000 / 하드캡 안전권", size=15, weight="bold", color="greenaccent"),
                ft.Text("전체 로스터 평균 득점력 (AVG 연산):", size=12),
                ft.Text("26.1 PPG", size=15, weight="bold", color="amber"),
            ]),
            bgcolor="black38", border_radius=12, padding=15, width=370
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("🔗 3-Way LEFT OUTER JOIN 탐색 결과", size=13, weight="bold"),
                ft.Text("LAL ➔ 르브론 제임스 ➔ $47.6M (시즌성적 매핑)", size=12),
                ft.Text("LAL ➔ 윤동욱 ➔ $12.5M (신규 계약 조인)", size=12),
            ]),
            bgcolor="surfacevariant", border_radius=12, padding=15, width=370
        )
    ], spacing=15, horizontal_alignment="center"))

ft.app(target=main)
