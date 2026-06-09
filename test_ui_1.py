import flet as ft

def main(page: ft.Page):
    page.title = "NBA Roster & Contract DBMS - 화면 1"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 700  
    mock_team = {
        "name": "Los Angeles Lakers", 
        "city": "Los Angeles", 
        "arena": "Crypto.com Arena", 
        "coach": "JJ Redick", 
        "logo": "/logo.png"  
    }

    page.add(ft.Column([
        # 1. 헤더 타이틀
        ft.Container(ft.Text("🏀 1. 구단 마스터 정보 조회", size=18, weight="bold", color="orangeaccent"), padding=5),
        
        # 2. 구단 마스터 정보 메인 카드 (ft.Row를 사용하여 왼쪽 이미지, 오른쪽 텍스트 가로 배치)
        ft.Container(
            content=ft.Row([
                # 왼쪽: assets 폴더에서 불러온 LA 레이커스 로고 이미지 배치
                ft.Image(src=mock_team["logo"], width=110, height=110, fit="contain", border_radius=8),
                # 오른쪽: 구단 텍스트 정보 배치
                ft.Column([
                    ft.Text(mock_team["name"], size=20, weight="bold"),
                    ft.Text(f"연고지: {mock_team['city']}", size=14, color="grey400"),
                ], alignment="center", spacing=5)
            ], alignment="start", spacing=20),
            bgcolor="black26", border_radius=12, padding=15, width=390
        ),
        
        # 3. 구단 상세 부가 정보 카드
        ft.Container(
            content=ft.Column([
                ft.Text(f"🏟️ 홈 아레나 : {mock_team['arena']}", size=13),
                ft.Text(f"👔 감독 커맨더 : {mock_team['coach']}", size=13),
                ft.Text("🏆 파이널 우승 : 총 17회 달성 (역대 최다 타이기록)", size=13),
            ], spacing=8),
            bgcolor="surfacevariant", border_radius=12, padding=15, width=390
        )
    ], spacing=15, horizontal_alignment="center"))


ft.app(target=main, assets_dir="assets")
