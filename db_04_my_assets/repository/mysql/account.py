import pandas as pd
from ..interfaces import IAccountRepository


class MySQLAccountRepository(IAccountRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS account (
                account_id   INT NOT NULL PRIMARY KEY,
                account_name VARCHAR(100) UNIQUE,
                brokerage    VARCHAR(100)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) AS cnt FROM account"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['cnt']

    def save(self, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] account 저장 시작')

        columns = list(df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT IGNORE INTO account ({fields}) VALUES ({placeholders})"

        # DataFrame 데이터를 튜플 리스트로 변환
        data_tuples = [tuple(x) for x in df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] account 저장 완료')

    def find_all(self) -> pd.DataFrame:
        query = "SELECT * FROM account ORDER BY account_id"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result) if result else pd.DataFrame(columns=['account_id', 'account_name', 'brokerage'])