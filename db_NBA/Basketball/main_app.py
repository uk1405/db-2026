import flet as ft
import duckdb
import os

# 1. 프로그램 구동 시 데이터베이스 파일이 아예 없다면 최초 1번 테이블 및 기본 데이터셋 세팅
db_exists = os.path.exists('dw_nba.duckdb')
con = duckdb.connect('dw_nba.duckdb')

if not db_exists:
    con.execute("CREATE TABLE IF NOT EXISTS nba_team_master (team_code VARCHAR(50) PRIMARY KEY, team_name VARCHAR(100) NOT NULL, city VARCHAR(100) NOT NULL, logo_url VARCHAR(225));")
    con.execute("CREATE TABLE IF NOT EXISTS nba_player (player_id VARCHAR(50) PRIMARY KEY, full_name VARCHAR(100) NOT NULL, position VARCHAR(50), draft_year INT);")
    con.execute("CREATE TABLE IF NOT EXISTS nba_contract_stat (player_id VARCHAR(50), team_code VARCHAR(50), ppg FLOAT, salary INT, PRIMARY KEY (player_id, team_code), FOREIGN KEY (player_id) REFERENCES nba_player(player_id), FOREIGN KEY (team_code) REFERENCES nba_team_master(team_code));")

    con.execute("INSERT OR IGNORE INTO nba_team_master VALUES ('LAL', 'Los Angeles Lakers', 'Los Angeles', 'logo.png');")
    con.execute("INSERT OR IGNORE INTO nba_player VALUES ('P001', '르브론 제임스', 'F', 2003), ('P002', '앤서니 데이비스', 'C', 2012), ('P003', '윤동욱 (Rookie)', 'G', 2026);")
    con.execute("INSERT OR IGNORE INTO nba_contract_stat VALUES ('P001', 'LAL', 25.7, 47600000), ('P002', 'LAL', 24.5, 43200000), ('P003', 'LAL', 28.1, 12500000);")
    con.commit()


def main(page: ft.Page):
    page.title = "NBA 통합 데이터베이스 관리 시스템 (DBMS)"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 480
    page.window_height = 750
    page.scroll = ft.ScrollMode.AUTO

    # -------------------------------------------------------------
    # [화면 1] 구단 마스터 정보 조회 레이아웃 구성
    # -------------------------------------------------------------
    team_logo = ft.Image(src="logo.png", width=110, height=110, fit="contain", border_radius=8)
    team_name_text = ft.Text("구단명: 선택되지 않음", size=20, weight=ft.FontWeight.BOLD)
    team_city_text = ft.Text("연고지: 선택되지 않음", size=14, color="grey400")
    team_arena_text = ft.Text("홈 아레나: 조회 전", size=13)
    team_coach_text = ft.Text("감독 커맨더: 조회 전", size=13)

    def on_team_select_clicked(e):
        target_team_code = "LAL"
        query = "SELECT team_name, city, logo_url FROM nba_team_master WHERE team_code = ?"
        result = con.execute(query, [target_team_code]).fetchone()
        if result:
            team_name_text.value = f"구단명: {result[0]}"
            team_city_text.value = f"연고지: {result[1]}"
            team_logo.src = result[2]
            team_arena_text.value = f"홈 아레나: Crypto.com Arena"
            team_coach_text.value = f"감독 커맨더: JJ Redick"
            page.update()

    ui_screen_1 = ft.Column([
        ft.Container(ft.Text("🏀 NBA 구단 정보 단건 조회", size=16, weight="bold", color="orangeaccent")),
        ft.Container(
            content=ft.Row([
                team_logo,
                ft.Column([team_name_text, team_city_text], alignment="center", spacing=5)
            ], alignment="start", spacing=20),
            bgcolor="black26", border_radius=12, padding=15, width=420
        ),
        ft.Container(content=ft.Column([team_arena_text, team_coach_text], spacing=5)),
        ft.ElevatedButton("구단 DB 정보 로드", on_click=on_team_select_clicked)
    ], spacing=15, horizontal_alignment="center")

    # -------------------------------------------------------------
    # [화면 2] 3-Way JOIN 복합 로스터 조회 레이아웃 구성
    # -------------------------------------------------------------
    roster_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("포지션")),
            ft.DataColumn(ft.Text("선수 실명")),
            ft.DataColumn(ft.Text("PPG")),
            ft.DataColumn(ft.Text("연봉")),
        ],
        rows=[],
        heading_row_color="black38",
        column_spacing=20
    )

    def load_composite_roster(e):
        target_team_code = "LAL"
        sql_join = """
            SELECT p.position, p.full_name, c.ppg, c.salary
            FROM nba_team_master t
            LEFT OUTER JOIN nba_contract_stat c ON t.team_code = c.team_code
            LEFT OUTER JOIN nba_player p ON c.player_id = p.player_id
            WHERE t.team_code = ?
            ORDER BY c.salary DESC
        """
        db_rows = con.execute(sql_join, [target_team_code]).fetchall()
        roster_table.rows.clear()
        for row in db_rows:
            roster_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(row[0] if row[0] else "-"))),
                        ft.DataCell(ft.Text(str(row[1] if row[1] else "공석"), weight="bold")),
                        ft.DataCell(ft.Text(f"{row[2]:.1f}" if row[2] else "0.0", color="amber")),
                        ft.DataCell(ft.Text(f"${row[3]:,}" if row[3] else "$0", color="greenaccent")),
                    ]
                )
            )
        page.update()

    ui_screen_2 = ft.Column([
        ft.Container(ft.Text("📋 소속 선수 로스터 (3-Way JOIN)", size=16, weight="bold", color="orangeaccent")),
        ft.ElevatedButton("3-Way JOIN 로스터 동적 조회 💾", on_click=load_composite_roster),
        ft.Container(content=roster_table, bgcolor="black26", border_radius=12, padding=5)
    ], spacing=15, horizontal_alignment="center")

    # -------------------------------------------------------------
    # [화면 3] 신규 유망주 정보 분할 삽입 (트랜잭션) 구성
    # -------------------------------------------------------------
    input_player_id = ft.TextField(label="선수 고유 ID 입력 (ex: P100)", width=220)
    input_full_name = ft.TextField(label="선수 실명 입력", width=220)
    input_position = ft.Dropdown(
        label="포지션 선택",
        options=[ft.dropdown.Option("G"), ft.dropdown.Option("F"), ft.dropdown.Option("C")],
        width=220
    )
    input_ppg = ft.TextField(label="예상 득점력(PPG) 입력", width=220)
    input_salary = ft.TextField(label="보장 연봉 규모($) 입력", width=220)

    def on_submit_transaction_clicked(e):
        if not input_player_id.value or not input_full_name.value or not input_position.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ ID, 이름, 포지션은 필수 항목입니다!"))
            page.snack_bar.open = True
            page.update()
            return

        con.execute("BEGIN TRANSACTION")
        try:
            con.execute("INSERT INTO nba_player VALUES (?, ?, ?, 2026)", [input_player_id.value, input_full_name.value, input_position.value])
            con.execute("INSERT INTO nba_contract_stat VALUES (?, 'LAL', ?, ?)", [input_player_id.value, float(input_ppg.value if input_ppg.value else 0.0), int(input_salary.value if input_salary.value else 0)])
            con.commit()
            page.snack_bar = ft.SnackBar(ft.Text("데이터베이스 원자적 분할 쓰기 트랜잭션 성공! 🎉"))
            page.snack_bar.open = True
        except Exception as error_msg:
            con.execute("ROLLBACK")
            page.snack_bar = ft.SnackBar(ft.Text(f"트랜잭션 오류 발생으로 전면 롤백: {str(error_msg)} ❌"))
            page.snack_bar.open = True
            
        input_player_id.value = ""
        input_full_name.value = ""
        input_position.value = None
        input_ppg.value = ""
        input_salary.value = ""
        page.update()

    ui_screen_3 = ft.Column([
        ft.Container(ft.Text("✨ 신규 유망주 분할 삽입 (CREATE)", size=16, weight="bold", color="orangeaccent")),
        input_player_id, input_full_name, input_position, input_ppg, input_salary,
        ft.ElevatedButton("신규 유망주 트랜잭션 등록 🚀", on_click=on_submit_transaction_clicked)
    ], spacing=10, horizontal_alignment="center")

    # -------------------------------------------------------------
    # [화면 4] 실시간 집계 연산 보정 및 복합 Join 구성
    # -------------------------------------------------------------
    sum_salary_text = ft.Text("$0 / 데이터 로드 전", size=15, weight="bold", color="greenaccent")
    avg_ppg_text = ft.Text("0.0 PPG", size=15, weight="bold", color="amber")
    join_result_column = ft.Column(spacing=8)

    def load_metrics_and_join(e):
        target_team_code = "LAL"
        metric_res = con.execute("SELECT SUM(salary), AVG(ppg) FROM nba_contract_stat WHERE team_code = ?", [target_team_code]).fetchone()
        
        if metric_res and metric_res[0] is not None:
            sum_salary_text.value = f"${int(metric_res[0]):,} / 하드캡 안전권"
            avg_ppg_text.value = f"{float(metric_res[1]):.1f} PPG"
        
        join_query = """
            SELECT t.team_code, p.full_name, c.salary
            FROM nba_team_master t
            LEFT OUTER JOIN nba_contract_stat c ON t.team_code = c.team_code
            LEFT OUTER JOIN nba_player p ON c.player_id = p.player_id
            WHERE t.team_code = ? ORDER BY c.salary DESC
        """
        join_rows = con.execute(join_query, [target_team_code]).fetchall()
        join_result_column.controls.clear()
        for row in join_rows:
            if row[1]:
                join_result_column.controls.append(ft.Text(f"🔗 {row[0]} ➔ {row[1]} ➔ ${row[2]/1000000:.1f}M (조인 성공)", size=12, color="white70"))
            else:
                join_result_column.controls.append(ft.Text(f"🔗 {row[0]} ➔ 소속 등록 선수 없음 (공석)", size=12, color="redaccent"))
        page.update()

    ui_screen_4 = ft.Column([
        ft.Container(ft.Text("📊 실시간 연산 보정 및 복합 Join", size=16, weight="bold", color="orangeaccent")),
        ft.ElevatedButton("실시간 통계 및 JOIN 데이터 연산 🚀", on_click=load_metrics_and_join),
        ft.Container(
            content=ft.Column([
                ft.Text("📈 샐러리캡 및 연산 보정 지표", size=14, weight="bold", color="grey300"),
                ft.Divider(color="grey700"),
                ft.Text("팀 샐러리캡 총합산 (SUM 연산):", size=11),
                sum_salary_text,
                ft.Text("전체 로스터 평균 득점력 (AVG 연산):", size=11),
                avg_ppg_text,
            ]), bgcolor="black38", border_radius=12, padding=15, width=420
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("🔗 3-Way LEFT OUTER JOIN 탐색 결과", size=13, weight="bold"),
                ft.Divider(color="grey600"),
                join_result_column
]), bgcolor="surfacevariant", border_radius=12, padding=15, width=420)], spacing=15, horizontal_alignment="center")# -------------------------------------------------------------# 🏁 메인 탭(Tabs) 레이아웃 생성 및 마스터 바인딩# -------------------------------------------------------------tabs = ft.Tabs(selected_index=0,animation_duration=300,tabs=[ft.Tab(text="구단 조회", icon=ft.Icons.GRID_VIEW, content=ft.Container(content=ui_screen_1, padding=20)),ft.Tab(text="로스터 조회", icon=ft.Icons.FORMAT_LIST_BULLETED, content=ft.Container(content=ui_screen_2, padding=20)),ft.Tab(text="유망주 등록", icon=ft.Icons.PERSON_ADD, content=ft.Container(content=ui_screen_3, padding=20)),ft.Tab(text="실시간 집계", icon=ft.Icons.BAR_CHART, content=ft.Container(content=ui_screen_4, padding=20)),],expand=1)page.add(tabs)ft.app(target=main)