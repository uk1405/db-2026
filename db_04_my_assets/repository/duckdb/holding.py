import pandas as pd
from ..interfaces import IHoldingRepository


class DuckDBHoldingRepository(IHoldingRepository):

    def create_table(self) -> None:
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS holding
            (
                ticker        VARCHAR NOT NULL, -- 티커
                account_id    INTEGER NOT NULL, -- 계좌 대리 키
                quantity      INTEGER,          -- 보유 주식 수
                avg_buy_price DOUBLE,           -- 매입 평균가
                PRIMARY KEY (ticker, account_id),
                FOREIGN KEY (ticker) REFERENCES asset (ticker),
                FOREIGN KEY (account_id) REFERENCES account (account_id)
            )
        """)

    def count(self) -> int:
        return self._con.execute("SELECT COUNT(*) FROM holding").fetchone()[0]

    def save(self, df: pd.DataFrame) -> None:
        self._con.execute("INSERT OR IGNORE INTO holding SELECT * FROM df")

    def find_all(self) -> pd.DataFrame:
        return self._con.execute("SELECT * FROM holding ORDER BY quantity DESC").df()

    def find_by_account(self, account_id: int) -> pd.DataFrame:
        """특정 계좌(account_id)가 보유한 주식 잔고 목록만 필터링"""
        query = "SELECT * FROM holding WHERE account_id = ? ORDER BY quantity DESC"
        return self._con.execute(query, [account_id]).df()
        