import duckdb
import pandas

# 데이터베이스 접속 (메모리 사용)
con = duckdb.connect()

# 테이블 생성
con.execute("""
    CREATE TABLE IF NOT EXISTS assets (
        ticker VARCHAR PRIMARY KEY,
        name VARCHAR,
        type VARCHAR
    )
""")

# 데이터 삽입
con.execute("""
    INSERT INTO assets VALUES 
        ('005930', '삼성전자', 'Stock'),
        ('000660', 'SK하이닉스', 'Stock'),
        ('148020', 'RISE 200', 'ETF'),
        ('360750', 'TIGER 미국S&P500', 'ETF'),
        ('379810', 'KODEX 미국나스닥100', 'ETF'),
        ('411060', 'ACE KRX 금현물', 'ETF'),
        ('449450', 'PLUS K방산', 'ETF')
""")

# 데이터 검색
df = con.execute("SELECT * FROM assets").df()
# con.close()

print(df)
# df