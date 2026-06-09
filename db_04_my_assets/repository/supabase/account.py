import pandas as pd
from ..interfaces import IAccountRepository


class SupabaseAccountRepository(IAccountRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS account (
                account_id   INT NOT NULL PRIMARY KEY,
                account_name VARCHAR(100) UNIQUE,
                brokerage    VARCHAR(100)
            );
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM account;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['count']

    def save(self, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] Supabase account 저장 시작')

        columns = list(df.columns)
        fields = ", ".join(columns)
        # PostgreSQL/Supabase는 파라미터 바인딩 플레이스홀더로 %s 사용
        placeholders = ", ".join(["%s"] * len(columns))
        
        # ON CONFLICT를 통해 중복 PK 발생 시 IGNORE 처리
        sql = f"INSERT INTO account ({fields}) VALUES ({placeholders}) ON CONFLICT (account_id) DO NOTHING;"

        data_tuples = [tuple(x) for x in df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] Supabase account 저장 완료')

    def find_all(self) -> pd.DataFrame:
        query = "SELECT account_id, account_name, brokerage FROM account ORDER BY account_id;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            cols = ['account_id', 'account_name', 'brokerage']
            return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)