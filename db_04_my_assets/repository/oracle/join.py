import pandas as pd
from ..interfaces import IJoinRepository, IDatabaseManager


class OracleJoinRepository(IJoinRepository):

    def __init__(self, db: IDatabaseManager):
        # 의존성 주입(DI)을 통해 전달받은 DB 매니저로부터 커넥션 객체 얻음
        self._con = db.get_connection()

    def find_all(self) -> pd.DataFrame:
        """
        Oracle 표준 LEFT JOIN을 활용하여 다중 테이블 데이터를 조회합니다.
        오라클 fetchall() 결과 구조에 맞춰 명확하게 컬럼명을 입힌 데이터프레임을 반환합니다.
        """
        columns = ['name', 'ticker', 'account', 'brokerage', 'quantity', 'avg_buy_price']
        
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
            return pd.DataFrame(result, columns=columns) if result else pd.DataFrame(columns=columns)