import pandas as pd
from ..interfaces import IDailyPriceRepository


class OracleDailyPriceRepository(IDailyPriceRepository):

    def create_table(self) -> None:
        """
        Oracle은 'CREATE TABLE IF NOT EXISTS'를 지원하지 않음 
        딕셔너리(USER_TABLES)를 조회하여 테이블이 없을 때 생성
        """
        check_query = "SELECT COUNT(*) FROM user_tables WHERE table_name = 'DAILY_PRICE'"
        
        create_query = """
            CREATE TABLE daily_price (
                ticker    VARCHAR2(50) NOT NULL,
                "DATE"    DATE NOT NULL,
                "OPEN"    BINARY_DOUBLE,
                high      BINARY_DOUBLE,
                low       BINARY_DOUBLE,
                "CLOSE"   BINARY_DOUBLE,
                volume    NUMBER(19),
                CONSTRAINT pk_daily_price PRIMARY KEY (ticker, "DATE"),
                CONSTRAINT fk_price_asset FOREIGN KEY (ticker) REFERENCES asset (ticker)
            )
        """
        # DATE, OPEN, CLOSE는 Oracle 예약어
        # 쌍따옴표(")로 감싸야 함
        with self._con.cursor() as cursor:
            cursor.execute(check_query)
            if cursor.fetchone()[0] == 0:
                cursor.execute(create_query)

    def count(self) -> int:
        query = "SELECT COUNT(*) FROM daily_price"
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0]

    def find_latest_date(self) -> str:
        query = 'SELECT MAX("DATE") FROM daily_price'
        with self._con.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()[0].date()
            # res = cursor.fetchone()[0]
            # print(f'[DEBUG] find_latest_date raw result: {res} (type: {type(res)})')
            # input()
            # if res:
            #     # oracledb가 반환한 datetime 객체를 문자열로 변환
            #     return res.strftime('%Y-%m-%d') if hasattr(res, 'strftime') else str(res)
            # return ""

    def save(self, ticker: str, df: pd.DataFrame) -> None:
        if df.empty:
            return
        print('[INFO] daily_price 저장 시작')

        temp_df = df.copy()
        temp_df["date"] = temp_df["date"].astype(str)
        temp_df["ticker"] = ticker  
        
        # 스키마 순서에 맞게 컬럼 재배치
        temp_df = temp_df[["ticker", "date", "open", "high", "low", "close", "volume"]]

        columns = list(temp_df.columns)
        
        # Oracle 컬럼 매핑 시 예약어 우회를 위해 date, open, close에 쌍따옴표 적용
        # fields = ", ".join([f'"{col}"' if col in ['date', 'open', 'close'] else col for col in columns])
        oracle_fields = []
        for col in columns:
            if col == 'date':
                oracle_fields.append('"DATE"')
            elif col == 'open':
                oracle_fields.append('"OPEN"')
            elif col == 'close':
                oracle_fields.append('"CLOSE"')
            else:
                oracle_fields.append(col)
                
        fields = ", ".join(oracle_fields)
        
        # Oracle 순서 기반 플레이스홀더 (:1, :2, ...) 생성
        # 날짜 컬럼(:2)은 TO_DATE(:2, 'YYYY-MM-DD')로 감싸서 매핑
        placeholders = ":1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6, :7"
        
        sql = f'INSERT /*+ IGNORE_ROW_ON_DUPKEY_INDEX(daily_price pk_daily_price) */ INTO daily_price ({fields}) VALUES ({placeholders})'

        data_tuples = [tuple(x) for x in temp_df.to_numpy()]

        with self._con.cursor() as cursor:
            cursor.executemany(sql, data_tuples)
        print('[INFO] daily_price 저장 완료')

    def find_by_date(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Oracle 문법의 BETWEEN 날짜 조회 수행 
        결과를 DataFrame으로 변환
        """
        columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'volume']
        
        # 오라클 조회 시에도 예약어(DATE, OPEN, CLOSE) 처리를 위해 쌍따옴표 적용
        query = """
            SELECT ticker, TO_CHAR("DATE", 'YYYY-MM-DD') AS "DATE", "OPEN", high, low, "CLOSE", volume 
            FROM daily_price 
            WHERE ticker = :1 
              AND "DATE" BETWEEN TO_DATE(:2, 'YYYY-MM-DD') AND TO_DATE(:3, 'YYYY-MM-DD')
            ORDER BY "DATE" DESC
        """
        with self._con.cursor() as cursor:
            cursor.execute(query, (ticker, start_date, end_date))
            result = cursor.fetchall()
            
            if result:
                return pd.DataFrame(result, columns=columns)
            return pd.DataFrame(columns=columns)