import pandas as pd
from ..interfaces import IAccountRepository


class DuckDBAccountRepository(IAccountRepository):

    def create_table(self) -> None:
        self._con.execute("""
            CREATE TABLE IF NOT EXISTS account
            (
                account_id   INTEGER NOT NULL PRIMARY KEY, -- [후보키] 계좌 대리 키 (Surrogate Key)
                account_name VARCHAR UNIQUE,               -- [후보키] 계좌 이름 (예, ISA, 연금저축)
                brokerage    VARCHAR                       -- 증권사 (예, 한국투자증권, 미래에셋증권)
            )
        """)

    def count(self) -> int:
        return self._con.execute("SELECT COUNT(*) FROM account").fetchone()[0]

    def save(self, df: pd.DataFrame) -> None:
        self._con.execute("INSERT OR IGNORE INTO account SELECT * FROM df")

    def find_all(self) -> pd.DataFrame:
        return self._con.execute("SELECT * FROM account").df()