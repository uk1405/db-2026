import pandas as pd
from ..interfaces import IAssetRepository


class DuckDBAssetRepository(IAssetRepository):

    def create_table(self) -> None:
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS asset
            (
                ticker VARCHAR NOT NULL PRIMARY KEY, -- 티커
                name   VARCHAR,                      -- 종목 이름
                type   VARCHAR,                      -- 주식 또는 ETF
                country VARCHAR                      -- 국가
            )
        """)

    def count(self) -> int:
        return self._con.execute("SELECT COUNT(*) FROM asset").fetchone()[0]

    def save(self, df: pd.DataFrame) -> None:
        self._con.execute("INSERT OR IGNORE INTO asset SELECT * FROM df")

    def find_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        """
        종목 이름(name) 또는 티커(ticker)에 키워드가 포함된 데이터 검색
        키워드가 없으면 전체 데이터 반환
        """
        if keyword:
            # SQL Injection 방지를 위해 parameter binding 사용
            query = """
                SELECT * FROM asset 
                WHERE name ILIKE ? OR ticker ILIKE ?
                LIMIT 200
            """
            search_pattern = f"%{keyword}%"
            return self._con.execute(query, [search_pattern, search_pattern]).df()
        
        return self._con.execute("SELECT * FROM asset LIMIT 200").df()