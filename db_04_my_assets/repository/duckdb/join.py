import pandas as pd
from ..interfaces import IJoinRepository, IDatabaseManager


class DuckDBJoinRepository(IJoinRepository):

    def __init__(self, db: IDatabaseManager):
        self._con = db.get_connection()

    def find_all(self) -> pd.DataFrame:
        """
        모든 종목-보유-계좌 join 데이터 검색
        """
        return self._con.execute("""
            SELECT name, s.ticker, account_name AS account, brokerage, quantity, avg_buy_price
            FROM account a
            LEFT JOIN holding h ON a.account_id = h.account_id
            LEFT JOIN asset s ON h.ticker = s.ticker
            ORDER BY a.account_id, quantity DESC
        """).df()