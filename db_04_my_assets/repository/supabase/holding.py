import pandas as pd
from ..interfaces import IHoldingRepository


class SupabaseHoldingRepository(IHoldingRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS holding (
                ticker        VARCHAR(50) NOT NULL,
                account_id    INT NOT NULL,
                quantity      INT,
                avg_buy_price DOUBLE PRECISION,
                PRIMARY KEY (ticker, account_id),
                FOREIGN KEY (ticker) REFERENCES asset (ticker),
                FOREIGN KEY (account_id) REFERENCES account (account_id)
            );
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM holding;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['count']

    def save(self, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] Supabase holding 저장 시작')

        columns = list(df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO holding ({fields}) VALUES ({placeholders}) ON CONFLICT (ticker, account_id) DO NOTHING;"

        data_tuples = [tuple(x) for x in df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] Supabase holding 저장 완료')

    def find_all(self) -> pd.DataFrame:
        query = "SELECT ticker, account_id, quantity, avg_buy_price FROM holding ORDER BY quantity DESC;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            cols = ['ticker', 'account_id', 'quantity', 'avg_buy_price']
            return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)