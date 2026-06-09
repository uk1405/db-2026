import pandas as pd
from ..interfaces import IJoinRepository, IDatabaseManager


class SupabaseJoinRepository(IJoinRepository):

    def __init__(self, db: IDatabaseManager):
        # 의존성 주입(DI)을 통해 전달받은 DB 매니저로부터 커넥션 객체 얻음
        self._con = db.get_connection()

    def find_all(self) -> pd.DataFrame:
        query = """
            SELECT s.name, s.ticker, a.account_name AS account, a.brokerage, h.quantity, h.avg_buy_price
            FROM account a
            LEFT JOIN holding h ON a.account_id = h.account_id
            LEFT JOIN asset s ON h.ticker = s.ticker
            ORDER BY a.account_id, h.quantity DESC;
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            cols = ['name', 'ticker', 'account', 'brokerage', 'quantity', 'avg_buy_price']
            return pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(columns=cols)