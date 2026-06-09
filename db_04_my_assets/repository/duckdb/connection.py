import os
import duckdb
from dotenv import load_dotenv
from ..interfaces import IDatabaseManager

# 환경 변수 로드
load_dotenv()


class DuckDBManager(IDatabaseManager):
    """DuckDB 커넥션 관리 클래스"""

    def __init__(self):
        # .env에서 DUCKDB_PATH를 읽어오고, 없을 경우 기본값으로 설정
        self._db_path = os.getenv("DUCKDB_PATH", "data/finance.db")
        self._con = None

        # 데이터베이스 파일이 위치할 data 폴더가 없다면 생성 
        db_dir = os.path.dirname(self._db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def get_connection(self) -> duckdb.DuckDBPyConnection:
        """
        현재 활성화된 DuckDB 커넥션 반환
        기존 연결이 없다면 새로 연결을 맺고, 있다면 기존 객체 재사용
        """
        if self._con is None:
            try:
                self._con = duckdb.connect(self._db_path)
            except Exception as e:
                raise ConnectionError(f"[ERROR] DuckDB 연결 실패 (경로: {self._db_path}): {e}")
        
        return self._con

    def close(self) -> None:
        """현재 열려 있는 DuckDB 커넥션 종료"""
        if self._con is not None:
            try:
                self._con.close()
            except Exception:
                pass
            finally:
                self._con = None