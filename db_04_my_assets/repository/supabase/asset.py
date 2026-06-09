import pandas as pd
from ..interfaces import IAssetRepository


class SupabaseAssetRepository(IAssetRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS asset (
                ticker  VARCHAR(50) NOT NULL PRIMARY KEY, -- 티커
                name    VARCHAR(255),                     -- 종목 이름
                type    VARCHAR(50),                      -- 주식 또는 ETF
                country VARCHAR(50)                       -- 국가
            );
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM asset;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            # # return cursor.fetchone()[0]
            # result = cursor.fetchone()
            # print(f'[DEBUG] asset count result: {result}')
            # return result[0] if result else 0
            return cursor.fetchone()['count']

    def save(self, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] Supabase asset 저장 시작')

        columns = list(df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        
        # 기본키인 ticker 중복 발생 시 데이터 IGNORE 처리
        sql = f"INSERT INTO asset ({fields}) VALUES ({placeholders}) ON CONFLICT (ticker) DO NOTHING;"

        data_tuples = [tuple(x) for x in df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] Supabase asset 저장 완료')

    def find_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        cols = ['ticker', 'name', 'type', 'country']
        
        if not keyword or not keyword.strip():
            query = """
                SELECT ticker, name, type, country 
                FROM asset 
                ORDER BY country, name 
                LIMIT 200;
            """
            with self._con.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)

        # PostgreSQL/Supabase는 대소문자 무시 검색을 위해 ILIKE 사용
        query = """
            SELECT ticker, name, type, country 
            FROM asset 
            WHERE name ILIKE %s 
               OR ticker ILIKE %s 
            LIMIT 200;
        """
        search_str = f"%{keyword.strip()}%"
        with self._con.cursor() as cursor:
            cursor.execute(query, (search_str, search_str))
            rows = cursor.fetchall()
            return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)