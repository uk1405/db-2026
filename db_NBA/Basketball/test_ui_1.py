import flet as ft
import os

def main(page: ft.Page):
    page.title = "NBA Roster & Contract DBMS - 화면 1"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 700  

    # ◀ [치트키] 현재 이 파이썬 파일(test_ui_1.py)이 있는 폴더에서 logo.png를 직접 찾습니다.
    # 이렇게 하면 assets_dir 설정이 꼬여도 컴퓨터 내부 진짜 주소로 강제 연동합니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_image_path = os.path.join(current_dir, "logo.png")

    mock_team = {
        "name": "Los Angeles Lakers", 
        "city": "Los Angeles", 
        "arena": "Crypto.com Arena", 
        "coach": "JJ Redick", 
        "logo": absolute_image_path  # ◀ 절대 경로 주소 매핑
    }

    page.add(ft.Column([
        # 1. 헤더 타이틀
        ft.Container(ft.Text("🏀 1. 구단 마스터 정보 조회", size=18, weight="bold", color="orangeaccent"), padding=5),
        
        # 2. 구단 마스터 정보 메인 카드 (ft.Row를 사용하여 왼쪽 이미지, 오른쪽 텍스트 가로 배치)
        ft.Container(
            content=ft.Row([
                # 왼쪽: 강제 로드한 로컬 시스템 내의 이미지 배치
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

# 복잡한 assets_dir 경로 추적 옵션을 끄고 클린 모드로 실행합니다.
ft.app(target=main)
