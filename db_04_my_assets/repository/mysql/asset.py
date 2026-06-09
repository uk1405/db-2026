import pandas as pd
from ..interfaces import IAssetRepository


class MySQLAssetRepository(IAssetRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS asset (
                ticker VARCHAR(10),
                name VARCHAR(255),
                type VARCHAR(10),
                country VARCHAR(10),
                PRIMARY KEY (ticker)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) AS cnt FROM asset"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['cnt']

    def save(self, df: pd.DataFrame) -> None:
        if df.empty:
            return

        columns = list(df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT IGNORE INTO asset ({fields}) VALUES ({placeholders})"

        data_tuples = [tuple(x) for x in df.to_numpy()]
        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)

    def find_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        if not keyword or not keyword.strip():
            query = """
                SELECT ticker, name, type, country
                FROM asset 
                ORDER BY country, name 
                LIMIT 200
            """
            with self._con.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return pd.DataFrame(result) if result else pd.DataFrame(columns=['country', 'ticker', 'name', 'type'])

        query = """
            SELECT ticker, name, type, country 
            FROM asset 
            WHERE LOWER(name) LIKE %s 
            OR LOWER(ticker) LIKE %s
            LIMIT 200
        """
        search_str = f"%{keyword.strip().lower()}%"
        with self._con.cursor() as cursor:
            cursor.execute(query, (search_str, search_str))
            result = cursor.fetchall()
            return pd.DataFrame(result) if result else pd.DataFrame(columns=['country', 'ticker', 'name', 'type'])