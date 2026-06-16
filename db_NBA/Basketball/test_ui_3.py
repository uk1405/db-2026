import flet as ft
import duckdb
import os

# 파일이 없을 때만 최초 1번 테이블과 기본 데이터셋을 세팅합니다.
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
    page.title = "NBA Roster & Contract DBMS - 화면 3"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 450
    page.window_height = 700

    input_player_id = ft.TextField(label="선수 고유 ID 입력 (ex: P100)", width=200)
    input_full_name = ft.TextField(label="선수 실명 입력", width=200)
    input_position = ft.Dropdown(
        label="포지션 선택",
        options=[ft.dropdown.Option("G"), ft.dropdown.Option("F"), ft.dropdown.Option("C")],
        width=200
    )
    input_ppg = ft.TextField(label="예상 득점력(PPG) 입력", width=200)
    input_salary = ft.TextField(label="보장 연봉 규모($) 입력", width=200)

    def on_submit_transaction_clicked(e):
        if not input_player_id.value or not input_full_name.value or not input_position.value:
            page.snack_bar = ft.SnackBar(ft.Text("❌ ID, 이름, 포지션은 필수 입력 항목입니다!"))
            page.snack_bar.open = True
            page.update()
            return

        con.execute("BEGIN TRANSACTION")
        try:
            insert_player_sql = """
                INSERT INTO nba_player (player_id, full_name, position, draft_year)
                VALUES (?, ?, ?, 2026)
            """
            con.execute(insert_player_sql, [
                input_player_id.value, 
                input_full_name.value, 
                input_position.value
            ])
            
            insert_contract_sql = """
                INSERT INTO nba_contract_stat (player_id, team_code, ppg, salary)
                VALUES (?, 'LAL', ?, ?)
            """
            con.execute(insert_contract_sql, [
                input_player_id.value, 
                float(input_ppg.value if input_ppg.value else 0.0), 
                int(input_salary.value if input_salary.value else 0)
            ])
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

    btn_submit = ft.ElevatedButton("신규 유망주 복합 트랜잭션 등록 🚀", on_click=on_submit_transaction_clicked)
    
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    ft.Text("✨ 3. 신규 유망주 분할 삽입 (CREATE)", size=18, weight="bold", color="orangeaccent"),
                    padding=5
                ),
                input_player_id, input_full_name, input_position, 
                input_ppg, input_salary, btn_submit
            ],
            spacing=10,
            horizontal_alignment="center"
        )
    )

ft.app(target=main)
