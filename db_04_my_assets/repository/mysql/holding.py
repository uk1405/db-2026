import pandas as pd
from ..interfaces import IHoldingRepository


class MySQLHoldingRepository(IHoldingRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS holding (
                ticker        VARCHAR(50) NOT NULL,
                account_id    INT NOT NULL,
                quantity      INT,
                avg_buy_price DOUBLE,
                PRIMARY KEY (ticker, account_id),
                FOREIGN KEY (ticker) REFERENCES asset (ticker),
                FOREIGN KEY (account_id) REFERENCES account (account_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) AS cnt FROM holding"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['cnt']

    def save(self, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] holding 저장 시작')

        columns = list(df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT IGNORE INTO holding ({fields}) VALUES ({placeholders})"

        data_tuples = [tuple(x) for x in df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] holding 저장 완료')

    def find_all(self) -> pd.DataFrame:
        query = "SELECT * FROM holding ORDER BY quantity DESC"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result) if result else pd.DataFrame(columns=['ticker', 'account_id', 'quantity', 'avg_buy_price'])