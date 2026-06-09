import pandas as pd
from ..interfaces import IAssetRepository


class OracleAssetRepository(IAssetRepository):

    def create_table(self) -> None:
        """
        Oracle은 'CREATE TABLE IF NOT EXISTS'를 지원하지 않음 
        딕셔너리(USER_TABLES)를 조회하여 테이블이 없을 때 생성
        """
        check_query = "SELECT COUNT(*) FROM user_tables WHERE table_name = 'ASSET'"
        
        create_query = """
            CREATE TABLE asset (
                ticker VARCHAR2(10),
                name VARCHAR2(255),
                type VARCHAR2(10),
                country VARCHAR2(10),
                CONSTRAINT pk_asset PRIMARY KEY (ticker)
            )
        """
        with self._con.cursor() as cursor:
            cursor.execute(check_query)
            if cursor.fetchone()[0] == 0:
                cursor.execute(create_query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM asset"
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

        columns = list(df.columns)
        fields = ", ".join(columns)
        
        # Oracle 순서 기반 플레이스홀더 (:1, :2, ...) 생성
        placeholders = ", ".join([f":{i+1}" for i in range(len(columns))])
        
        # 기본키(PK) 중복 시 무시하고 넘어가는 힌트 적용
        sql = f"INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX(asset pk_asset) */ INTO asset ({fields}) VALUES ({placeholders})"

        data_tuples = [tuple(x) for x in df.to_numpy()]
        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)

    def find_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        """
        Oracle은 'LIMIT 200' 대신 'FETCH FIRST 200 ROWS ONLY' 문법 사용
        fetchall() 결과는 튜플 리스트로 반환
        Pandas DataFrame 생성 시 컬럼명 지정
        """
        columns = ['ticker', 'name', 'type', 'country']

        if not keyword or not keyword.strip():
            query = """
                SELECT ticker, name, type, country
                FROM asset 
                ORDER BY country, name 
                FETCH FIRST 200 ROWS ONLY
            """
            with self._con.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return pd.DataFrame(result, columns=columns) if result else pd.DataFrame(columns=columns)

        # Oracle 플레이스홀더 :1, :2 사용
        query = """
            SELECT ticker, name, type, country 
            FROM asset 
            WHERE LOWER(name) LIKE :1 
            OR LOWER(ticker) LIKE :2
            FETCH FIRST 200 ROWS ONLY
        """
        search_str = f"%{keyword.strip().lower()}%"
        with self._con.cursor() as cursor:
            cursor.execute(query, (search_str, search_str))
            result = cursor.fetchall()
            return pd.DataFrame(result, columns=columns) if result else pd.DataFrame(columns=columns)