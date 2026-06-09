import pandas as pd
from ..interfaces import IDailyPriceRepository


class SupabaseDailyPriceRepository(IDailyPriceRepository):

    def create_table(self) -> None:
        query = """
            CREATE TABLE IF NOT EXISTS daily_price (
                ticker VARCHAR(50) NOT NULL,
                date   DATE NOT NULL,
                open   DOUBLE PRECISION,
                high   DOUBLE PRECISION,
                low    DOUBLE PRECISION,
                close  DOUBLE PRECISION,
                volume BIGINT,
                PRIMARY KEY (ticker, date),
                FOREIGN KEY (ticker) REFERENCES asset (ticker)
            );
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM daily_price;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['count']

    def find_latest_date(self) -> str:
        query = "SELECT MAX(date) AS max_date FROM daily_price;"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()['max_date']
            # result = cursor.fetchone()['max_date']
            # # PostgreSQL DATE 결과가 datetime.date 객체일 수 있으므로 포맷팅 처리
            # if result:
            #     return result.strftime('%Y-%m-%d') if hasattr(result, 'strftime') else str(result)
            # return ""

    def save(self, ticker: str, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] Supabase daily_price 저장 시작')

        temp_df = df.copy()
        temp_df["date"] = temp_df["date"].astype(str)
        temp_df["ticker"] = ticker  
        
        temp_df = temp_df[["ticker", "date", "open", "high", "low", "close", "volume"]]

        columns = list(temp_df.columns)
        fields = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO daily_price ({fields}) VALUES ({placeholders}) ON CONFLICT (ticker, date) DO NOTHING;"

        data_tuples = [tuple(x) for x in temp_df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] Supabase daily_price 저장 완료')

    def find_by_date(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        query = """
            SELECT ticker, date, open, high, low, close, volume 
            FROM daily_price 
            WHERE ticker = %s 
              AND date BETWEEN %s AND %s
            ORDER BY date DESC;
        """
        with self._con.cursor() as cursor:
            cursor.execute(query, (ticker, start_date, end_date))
            rows = cursor.fetchall()
            cols = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
            
            if rows:
                df_result = pd.DataFrame(rows, columns=cols)
                df_result['date'] = df_result['date'].astype(str)
                return df_result
            return pd.DataFrame(columns=cols)