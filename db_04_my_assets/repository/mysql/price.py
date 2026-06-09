import pandas as pd
from ..interfaces import IDailyPriceRepository


class MySQLDailyPriceRepository(IDailyPriceRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS daily_price (
                ticker VARCHAR(50) NOT NULL,
                date   DATE NOT NULL,
                open   DOUBLE,
                high   DOUBLE,
                low    DOUBLE,
                close  DOUBLE,
                volume BIGINT,
                PRIMARY KEY (ticker, date),
                FOREIGN KEY (ticker) REFERENCES asset (ticker)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) AS cnt FROM daily_price"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['cnt']

    def find_latest_date(self) -> str:
        query = "SELECT MAX(date) AS max_date FROM daily_price"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['max_date']
            # result = cursor.fetchone()
            # # DATE 객체를 문자열로 변환
            # if result and result['max_date']:
            #     return result['max_date'].strftime('%Y-%m-%d') if hasattr(result['max_date'], 'strftime') else str(result['max_date'])
            # return ""

    def save(self, ticker: str, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] daily_price 저장 시작')

        temp_df = df.copy()
        temp_df["date"] = temp_df["date"].astype(str)
        temp_df["ticker"] = ticker  
        
        # 스키마 순서에 맞게 컬럼 재배치
        temp_df = temp_df[["ticker", "date", "open", "high", "low", "close", "volume"]]

        columns = list(temp_df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT IGNORE INTO daily_price ({fields}) VALUES ({placeholders})"

        data_tuples = [tuple(x) for x in temp_df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] daily_price 저장 완료')

    def find_by_date(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        query = """
            SELECT ticker, date, open, high, low, close, volume 
            FROM daily_price 
            WHERE ticker = %s 
              AND date BETWEEN %s AND %s
            ORDER BY date DESC
        """
        with self._con.cursor() as cursor:
            cursor.execute(query, (ticker, start_date, end_date))
            result = cursor.fetchall()
            
            if result:
                df_result = pd.DataFrame(result)
                # DATE 객체를 문자열로 변환
                if 'date' in df_result.columns:
                    df_result['date'] = df_result['date'].astype(str)
                return df_result
            return pd.DataFrame(columns=['ticker', 'date', 'open', 'high', 'low', 'close', 'volume'])