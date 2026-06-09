import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from ..interfaces import IDatabaseManager

# 환경 변수 로드
load_dotenv()


class SupabaseManager(IDatabaseManager):
    """Supabase (PostgreSQL) 커넥션 관리 클래스"""

    def __init__(self):
        # .env에서 Supabase PostgreSQL 접속 정보 로드
        self._host = os.getenv("SUPABASE_HOST")
        self._port = int(os.getenv("SUPABASE_PORT", "5432"))
        self._user = os.getenv("SUPABASE_USER")
        self._password = os.getenv("SUPABASE_PASSWORD")
        self._db = os.getenv("SUPABASE_DB", "postgres")
        
        self._con = None

    def get_connection(self):
        """
        현재 활성화된 Supabase 커넥션 반환
        기존 연결이 있다면 객체 재사용
        """
        if self._con is None or self._con.closed != 0:
            self._create_new_connection()
        else:
            try:
                # 커넥션이 정상적으로 작동하는지 가벼운 테스트 쿼리 전송
                with self._con.cursor() as cursor:
                    cursor.execute("SELECT 1")
            except Exception:
                # 연결에 문제(Timeout 등)가 있다면 새로 커넥션 생성
                self._create_new_connection()

        return self._con

    def _create_new_connection(self) -> None:
        """Supabase PostgreSQL 서버와 커넥션 생성"""
        try:
            self._con = psycopg2.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                dbname=self._db,
                # MySQL의 DictCursor처럼 결과를 딕셔너리 형태로 받기 위함
                cursor_factory=RealDictCursor
            )
            # 트랜잭션 자동 반영 (Auto-commit) 설정
            self._con.autocommit = True
            
        except Exception as e:
            raise ConnectionError(
                f"Supabase PostgreSQL 연결에 실패했습니다. (Host: {self._host}:{self._port}): {e}"
            )

    def close(self) -> None:
        """현재 열려 있는 Supabase 커넥션 종료"""
        if self._con is not None and self._con.closed == 0:
            try:
                self._con.close()
            except Exception:
                pass
            finally:
                self._con = None
