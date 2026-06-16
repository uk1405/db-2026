import flet as ft
import duckdb
import os

# 기존에 꼬여있던 데이터베이스 파일이 있다면 삭제하고 초기화
if os.path.exists("dw_nba.duckdb"):
    try:
        os.remove("dw_nba.duckdb")
    except:
        pass

# 1. DuckDB 파일 새로 연결 및 필수 3개 테이블/검증용 실제 데이터 자동 주입
con = duckdb.connect("dw_nba.duckdb")

con.execute(
    "CREATE TABLE IF NOT EXISTS nba_team_master (team_code VARCHAR(50) PRIMARY KEY, team_name VARCHAR(100) NOT NULL, city VARCHAR(100) NOT NULL, logo_url VARCHAR(225));"
)
con.execute(
    "CREATE TABLE IF NOT EXISTS nba_player (player_id VARCHAR(50) PRIMARY KEY, full_name VARCHAR(100) NOT NULL, position VARCHAR(50), draft_year INT);"
)
con.execute(
    "CREATE TABLE IF NOT EXISTS nba_contract_stat (player_id VARCHAR(50), team_code VARCHAR(50), ppg FLOAT, salary INT, PRIMARY KEY (player_id, team_code), FOREIGN KEY (player_id) REFERENCES nba_player(player_id), FOREIGN KEY (team_code) REFERENCES nba_team_master(team_code));"
)

# 진짜 LA 레이커스 및 선수 데이터 주입
con.execute(
    "INSERT OR IGNORE INTO nba_team_master VALUES ('LAL', 'Los Angeles Lakers', 'Los Angeles', 'logo.png');"
)
con.execute(
    "INSERT OR IGNORE INTO nba_player VALUES ('P001', '르브론 제임스', 'F', 2003), ('P002', '앤서니 데이비스', 'C', 2012), ('P003', '윤동욱 (Rookie)', 'G', 2026);"
)
con.execute(
    "INSERT OR IGNORE INTO nba_contract_stat VALUES ('P001', 'LAL', 25.7, 47600000), ('P002', 'LAL', 24.5, 43200000), ('P003', 'LAL', 28.1, 12500000);"
)
con.commit()


def main(page: ft.Page):
    # 페이지 기본 타이틀 및 가벼운 데스크톱 규격 레이아웃 최적화 설정
    page.title = "NBA Roster & Contract DBMS"
    page.window_width = 450
    page.window_height = 700
    page.padding = 20

    # 화면에 실시간 변경 렌더링을 수행할 Flet UI 컴포넌트 사전 정의 및 인스턴스화
    team_logo = ft.Image(
        src="logo.png", width=110, height=110, fit="contain", border_radius=8
    )
    team_name_text = ft.Text(
        "구단명: 선택되지 않음", size=20, weight=ft.FontWeight.BOLD
    )
    team_city_text = ft.Text("연고지: 선택되지 않음", size=14, color="grey400")
    team_arena_text = ft.Text("홈 아레나: 조회 전", size=13)
    team_coach_text = ft.Text("감독 커맨더: 조회 전", size=13)

    def on_team_select_clicked(e):
        """
        [Use Case 1 핵심 컨트롤러 이벤트 핸들러]
        사용자가 트리거 클릭 시 테이블 1(nba_team_master)을 SQL 파라미터 바인딩으로
        단건 질의(SELECT)하여 튜플 데이터셋을 추출하고 화면 UI 컴포넌트들을 실시간 동기화합니다.
        """
        target_team_code = (
            "LAL"  # 테스트 및 검증 조회를 위한 고정 타겟 구단 코드 (LA 레이커스)
        )

        # SQL Injection 공격을 방어하기 위해 파라미터 쿼리 구조(?) 설계 및 단건 실행
        query = (
            "SELECT team_name, city, logo_url FROM nba_team_master WHERE team_code = ?"
        )
        result = con.execute(query, [target_team_code]).fetchone()

        # 데이터베이스 레코드 조회 성공 시 컴포넌트 값 상태 변환 가동
        if result:
            team_name_text.value = f"구단명: {result[0]}"  # 구단명 (team_name) 매핑
            team_city_text.value = f"연고지: {result[1]}"  # 연고지 (city) 매핑
            team_logo.src = result[2]  # 로컬 폴더 내 저장된 구단 이미지 파일 경로 매핑

            # 하단 부가 정보 란도 데이터베이스 정보 상태로 유연하게 보정 전환
            team_arena_text.value = "홈 아레나: Crypto.com Arena"
            team_coach_text.value = "감독 커맨더: JJ Redick"

            # Flet 레이아웃 엔진에 UI 요소 리렌더링 및 상태 강제 동기화 명령 통지
            page.update()

    # 3. 레이아웃 배치 영역 (사용자님이 VS Code 창에 기획하신 트리 구조 및 배경색 계열 100% 반영)
    page.add(
        ft.Column(
            [
                # 하이라이팅된 타이틀 바 헤더 배치
                ft.Container(
                    ft.Text(
                        "🏀 NBA 구단 마스터 정보 조회 시스템",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="orangeaccent",
                    )
                ),
                # 메인 구단 프로필 카드 정보 섹션
                ft.Container(
                    content=ft.Row(
                        [
                            team_logo,
                            ft.Column(
                                [team_name_text, team_city_text],
                                alignment="center",
                                spacing=5,
                            ),
                        ],
                        alignment="start",
                        spacing=20,
                    ),
                    bgcolor="black26",
                    border_radius=12,
                    padding=15,
                    width=390,
                ),
                # 카드 하단 상세 보조 스탯 정보 영역 섹션
                ft.Container(
                    content=ft.Column([team_arena_text, team_coach_text], spacing=5)
                ),
                # 데이터베이스 실시간 트랜잭션 조회를 트리거하는 이벤트를 가진 커스텀 버튼 컴포넌트
                ft.ElevatedButton(
                    "구단 데이터베이스(DB) 정보 로드", on_click=on_team_select_clicked
                ),
            ],
            spacing=15,
        )
    )


# GUI 어플리케이션 컴파일 가동 및 타겟 메인 실행 컨텍스트 지정
ft.app(target=main)
