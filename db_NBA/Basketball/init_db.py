import duckdb

# 1. 데이터베이스 파일 연결 (없으면 새로 자동 생성됨)
con = duckdb.connect('dw_nba.duckdb')

print("데이터베이스 초기화 시작...")

# 2. 기존 테이블이 있다면 초기화를 위해 삭제 (깔끔하게 새로 고침)
con.execute("DROP TABLE IF EXISTS nba_contract_stat;")
con.execute("DROP TABLE IF EXISTS nba_player;")
con.execute("DROP TABLE IF EXISTS nba_team_master;")

# 3. 3개 핵심 테이블 생성
con.execute("""
CREATE TABLE nba_team_master (
    team_code VARCHAR(50) PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    logo_url VARCHAR(225)
);
""")

con.execute("""
CREATE TABLE nba_player (
    player_id VARCHAR(50) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    position VARCHAR(50),
    draft_year INT
);
""")

con.execute("""
CREATE TABLE nba_contract_stat (
    player_id VARCHAR(50),
    team_code VARCHAR(50),
    ppg FLOAT,
    salary INT,
    PRIMARY KEY (player_id, team_code),
    FOREIGN KEY (player_id) REFERENCES nba_player(player_id),
    FOREIGN KEY (team_code) REFERENCES nba_team_master(team_code)
);
""")

print("테이블 생성 완료!")

# 4. 실제 검증용 NBA 데이터 삽입 (INSERT)
con.execute("""
INSERT INTO nba_team_master (team_code, team_name, city, logo_url) 
VALUES ('LAL', 'Los Angeles Lakers', 'Los Angeles', 'logo.png');
""")

con.execute("""
INSERT INTO nba_player (player_id, full_name, position, draft_year) VALUES 
('P001', '르브론 제임스', 'F', 2003),
('P002', '앤서니 데이비스', 'C', 2012),
('P003', '윤동욱 (Rookie)', 'G', 2026);
""")

con.execute("""
INSERT INTO nba_contract_stat (player_id, team_code, ppg, salary) VALUES 
('P001', 'LAL', 25.7, 47600000),
('P002', 'LAL', 24.5, 43200000),
('P003', 'LAL', 28.1, 12500000);
""")

# 변경 사항 영구 저장 후 닫기
con.commit()
con.close()

print("모든 실제 데이터 입력 성공! 이제 Flet 앱을 실행하시면 데이터가 뜹니다.")
