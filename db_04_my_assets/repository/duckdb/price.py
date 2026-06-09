import pandas as pd
from ..interfaces import IDailyPriceRepository


class DuckDBDailyPriceRepository(IDailyPriceRepository):

    def create_table(self) -> None:
        """daily_price 테이블 생성 (DDL)"""
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS daily_price
            (
                ticker VARCHAR NOT NULL, -- 티커
                date   DATE    NOT NULL, -- 날짜
                open   DOUBLE,           -- 시작가
                high   DOUBLE,           -- 최고가
                low    DOUBLE,           -- 최저가
                close  DOUBLE,           -- 종가
                volume BIGINT,           -- 거래량
                PRIMARY KEY (ticker, date),
                FOREIGN KEY (ticker) REFERENCES asset (ticker)
            )
        """)

    def count(self) -> int:
        return self._con.execute("SELECT COUNT(*) FROM daily_price").fetchone()[0]

    def find_latest_date(self) -> str:
        """
        테이블에 저장된 가장 최근 시세 날짜 반환
        """
        return self._con.execute("SELECT MAX(date) FROM daily_price").fetchone()[0]

    def save(self, ticker: str, df: pd.DataFrame) -> None:
        df["date"] = df["date"].astype(str) # 날짜를 문자열로 변환 (DuckDB는 DATE 타입을 문자열로 받음)
        df["ticker"] = ticker  # ticker 컬럼 추가

        # daily_price 테이블의 스키마에 맞게 컬럼 순서 조정
        df = df[["ticker", "date", "open", "high", "low", "close", "volume"]]

        self._con.execute("INSERT OR IGNORE INTO daily_price SELECT * FROM df")

    def find_by_date(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str
    ) -> pd.DataFrame:
        """
        특정 티커의 특정 기간의 시세 데이터 검색
        """
        return self._con.execute("""
            SELECT * 
            FROM daily_price 
            WHERE ticker = ? 
            AND date BETWEEN ? AND ?
            ORDER BY date DESC
        """, [ticker, start_date, end_date]).df()