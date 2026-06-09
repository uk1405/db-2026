import pandas as pd
from ..interfaces import IJoinRepository, IDatabaseManager


class MySQLJoinRepository(IJoinRepository):

    def __init__(self, db: IDatabaseManager):
        self._con = db.get_connection()

    def find_all(self) -> pd.DataFrame:
        query = """
            SELECT s.name, s.ticker, a.account_name AS account, a.brokerage, h.quantity, h.avg_buy_price
            FROM account a
            LEFT JOIN holding h ON a.account_id = h.account_id
            LEFT JOIN asset s ON h.ticker = s.ticker
            ORDER BY a.account_id, h.quantity DESC
        """
        with self._con.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result) if result else pd.DataFrame(columns=['name', 'ticker', 'account', 'brokerage', 'quantity', 'avg_buy_price'])