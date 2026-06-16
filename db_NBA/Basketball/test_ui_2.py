import flet as ft
import duckdb
import os

# 🎯 [수정 완료] 기존 DB를 무조건 지우던 os.remove 로직을 완전히 제거했습니다.
# 파일이 없을 때만 최초 1번 테이블을 만들고 기본 데이터를 채워넣습니다.
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
    page.title = "NBA Roster & Contract DBMS - 화면 2"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 650
    page.scroll = ft.ScrollMode.AUTO

    roster_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("포지션")),
            ft.DataColumn(ft.Text("선수 실명")),
            ft.DataColumn(ft.Text("PPG")),
            ft.DataColumn(ft.Text("연봉")),
        ],
        rows=[],
        heading_row_color="black38",
        column_spacing=25
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
                        ft.DataCell(ft.Text(f"{row[2]:.1f}" if row[2] else "0.0", color="amber")), # 소수점 깔끔하게 1자리 보정
                        ft.DataCell(ft.Text(f"${row[3]:,}" if row[3] else "$0", color="greenaccent")),
                    ]
                )
            )
        page.update()

    page.add(
        ft.Column([
            ft.Container(
                ft.Text("📋 2. 소속 계약 선수 로스터 (3-Way JOIN)", size=18, weight="bold", color="orangeaccent"), 
                padding=5
            ),
            ft.ElevatedButton("3-Way JOIN 로스터 동적 조회 💾", on_click=load_composite_roster),
            ft.Container(
                content=roster_table,
                bgcolor="black26", 
                border_radius=12, 
                padding=5
            )
        ], spacing=10, horizontal_alignment="center")
    )

ft.app(target=main)
