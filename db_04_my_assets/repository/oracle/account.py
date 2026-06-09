import pandas as pd
from ..interfaces import IAccountRepository


class OracleAccountRepository(IAccountRepository):

    def create_table(self) -> None:
        """
        Oracle은 'CREATE TABLE IF NOT EXISTS'를 지원하지 않음 
        딕셔너리(USER_TABLES)를 조회하여 테이블이 없을 때 생성
        """
        check_query = "SELECT COUNT(*) FROM user_tables WHERE table_name = 'ACCOUNT'"
        
        create_query = """
            CREATE TABLE account (
                account_id   NUMBER NOT NULL,
                account_name VARCHAR2(100),
                brokerage    VARCHAR2(100),
                CONSTRAINT pk_account PRIMARY KEY (account_id),
                CONSTRAINT uq_account_name UNIQUE (account_name)
            )
        """
        with self._con.cursor() as cursor:
            cursor.execute(check_query)
            if cursor.fetchone()[0] == 0:
                cursor.execute(create_query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM account"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def save(self, df: pd.DataFrame) -> None:
        """
        Oracle은 'INSERT IGNORE' 대신 'MERGE INTO' 구문 사용, 또는
        'INSERT' 중 발생하는 기본키 중복 에러(ORA-00001)를 무시(IGNORE)하는 힌트 사용.
        INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX */ 힌트 적용
        """
        if df.empty:
            return
        print('[INFO] account 저장 시작')

        columns = list(df.columns)
        fields = ", ".join(columns)
        
        # Oracle 순서 기반 플레이스홀더 (:1, :2, ...) 생성
        placeholders = ", ".join([f":{i+1}" for i in range(len(columns))])
        
        # primary key 제약조건명(pk_account)을 지정하여 중복 데이터 무시 힌트 적용
        sql = f"INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX(account pk_account) */ INTO account ({fields}) VALUES ({placeholders})"

        # DataFrame 데이터를 튜플 리스트로 변환
        data_tuples = [tuple(x) for x in df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] account 저장 완료')

    def find_all(self) -> pd.DataFrame:
        """
        fetchall() 결과는 튜플 리스트로 반환
        Pandas DataFrame 생성 시 컬럼명 지정
        """
        columns = ['account_id', 'account_name', 'brokerage']
        query = "SELECT account_id, account_name, brokerage FROM account ORDER BY account_id"
        
        with self._con.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return pd.DataFrame(result, columns=columns) if result else pd.DataFrame(columns=columns)