import flet as ft
import duckdb
import os

# [강제 조치] 기존에 꼬여있던 데이터베이스 파일이 있다면 완벽하게 제거하고 새로 시작
if os.path.exists('dw_nba.duckdb'):
    try:
        os.remove('dw_nba.duckdb')
    except:
        pass

# 1. DuckDB 파일 연결 및 테이블/실제 검증용 데이터 자동 주입
con = duckdb.connect('dw_nba.duckdb')

con.execute("CREATE TABLE IF NOT EXISTS nba_team_master (team_code VARCHAR(50) PRIMARY KEY, team_name VARCHAR(100) NOT NULL, city VARCHAR(100) NOT NULL, logo_url VARCHAR(225));")
con.execute("CREATE TABLE IF NOT EXISTS nba_player (player_id VARCHAR(50) PRIMARY KEY, full_name VARCHAR(100) NOT NULL, position VARCHAR(50), draft_year INT);")
con.execute("CREATE TABLE IF NOT EXISTS nba_contract_stat (player_id VARCHAR(50), team_code VARCHAR(50), ppg FLOAT, salary INT, PRIMARY KEY (player_id, team_code), FOREIGN KEY (player_id) REFERENCES nba_player(player_id), FOREIGN KEY (team_code) REFERENCES nba_team_master(team_code));")

con.execute("INSERT OR IGNORE INTO nba_team_master VALUES ('LAL', 'Los Angeles Lakers', 'Los Angeles', 'logo.png');")
con.execute("INSERT OR IGNORE INTO nba_player VALUES ('P001', '르브론 제임스', 'F', 2003), ('P002', '앤서니 데이비스', 'C', 2012), ('P003', '윤동욱 (Rookie)', 'G', 2026);")
con.execute("INSERT OR IGNORE INTO nba_contract_stat VALUES ('P001', 'LAL', 25.7, 47600000), ('P002', 'LAL', 24.5, 43200000), ('P003', 'LAL', 28.1, 12500000);")
con.commit()


def main(page: ft.Page):
    page.title = "NBA Roster & Contract DBMS - 화면 4"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 450
    page.window_height = 650

    # 실시간 데이터베이스 집계 연산 결과를 출력할 UI 컴포넌트 사전 정의
    sum_salary_text = ft.Text("$0 / 데이터 로드 전", size=15, weight="bold", color="greenaccent")
    avg_ppg_text = ft.Text("0.0 PPG", size=15, weight="bold", color="amber")
    
    # 조인 탐색 결과 리스트 컨테이너
    join_result_column = ft.Column(spacing=8)

    def load_metrics_and_join(e):
        target_team_code = "LAL"
        
        # [작동 1] SQL 집계 함수(SUM, AVG) 실시간 쿼리 실행
        metric_res = con.execute("SELECT SUM(salary), AVG(ppg) FROM nba_contract_stat WHERE team_code = ?", [target_team_code]).fetchone()
        
        # 🎯 [인덱스 수정 완벽 보정] metric_res[0]과 metric_res[1]로 튜플 값 조절
        if metric_res and metric_res[0] is not None:
            total_salary = int(metric_res[0])
            average_ppg = float(metric_res[1])
            
            # 대시보드 텍스트 상태 변경 적용
            sum_salary_text.value = f"${total_salary:,} / 하드캡 안전권"
            avg_ppg_text.value = f"{average_ppg:.1f} PPG"
        
        # [작동 2] 3-Way LEFT OUTER JOIN 명세 매핑 탐색
        join_query = """
            SELECT t.team_code, p.full_name, c.salary
            FROM nba_team_master t
            LEFT OUTER JOIN nba_contract_stat c ON t.team_code = c.team_code
            LEFT OUTER JOIN nba_player p ON c.player_id = p.player_id
            WHERE t.team_code = ?
            ORDER BY c.salary DESC
        """
        join_rows = con.execute(join_query, [target_team_code]).fetchall()
        
        join_result_column.controls.clear()
        for row in join_rows:
            # 🎯 [인덱스 수정 완벽 보정] row[0], row[1], row[2]로 각 컬럼 값 매핑
            if row[1]:
                salary_million = row[2] / 1000000
                join_result_column.controls.append(
                    ft.Text(f"🔗 {row[0]} ➔ {row[1]} ➔ ${salary_million:.1f}M (계약 조인 성공)", size=12, color="white70")
                )
            else:
                join_result_column.controls.append(
                    ft.Text(f"🔗 {row[0]} ➔ 소속 등록 선수 없음 (공석)", size=12, color="redaccent")
                )
        
        page.update()

    # 레이아웃 배치 영역
    page.add(ft.Column([
        ft.Container(ft.Text("📊 4. 실시간 연산 보정 및 복합 Join", size=18, weight="bold", color="orangeaccent"), padding=5),
        ft.ElevatedButton("실시간 통계 및 JOIN 데이터 연산 🚀", on_click=load_metrics_and_join),
        ft.Container(
            content=ft.Column([
                ft.Text("📈 샐러리캡 및 연산 보정 지표", size=14, weight="bold", color="grey300"),
                ft.Divider(color="grey700"),
                ft.Text("팀 샐러리캡 총합산 (SUM 연산):", size=12),
                sum_salary_text,
                ft.Text("전체 로스터 평균 득점력 (AVG 연산):", size=12),
                avg_ppg_text,
            ]),
            bgcolor="black38", border_radius=12, padding=15, width=370
        ),
        ft.Container(
            content=ft.Column([
                ft.Text("🔗 3-Way LEFT OUTER JOIN 탐색 결과", size=13, weight="bold"),
                ft.Divider(color="grey600"),
                join_result_column
            ]),
            bgcolor="surfacevariant", border_radius=12, padding=15, width=370
        )
    ], spacing=15, horizontal_alignment="center"))

ft.app(target=main)
