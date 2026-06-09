import os
import oracledb
from dotenv import load_dotenv
from ..interfaces import IDatabaseManager

# 환경 변수 로드
load_dotenv()


class OracleManager(IDatabaseManager):
    """Oracle 커넥션 관리 클래스"""

    def __init__(self):
        # .env에서 Oracle 접속 정보 로드
        host = os.getenv("ORACLE_HOST", "localhost")
        port = int(os.getenv("ORACLE_PORT", 1521))
        user = os.getenv("ORACLE_USER", "system")
        password = os.getenv("ORACLE_PASSWORD", "password")
        service_name = os.getenv("ORACLE_SERVICE_NAME", "XE")

        try:
            # Oracle Thin 모드로 접속 시도
            self._con = oracledb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                service_name=service_name
            )
            # MySQL의 autocommit=True와 맞추기 위해 세팅
            self._con.autocommit = True
            
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            raise ConnectionError(
                f"[ERROR] Oracle 연결 실패 (Host: {host}:{port}, Service: {service_name}): [ORA-{error_obj.code}] {error_obj.message}"
            )

    def get_connection(self) -> oracledb.Connection:
        """
        현재 활성화된 Oracle 커넥션 반환
        기존 연결이 있다면 객체 재사용
        """
        return self._con

    def close(self) -> None:
        """현재 열려 있는 Oracle 커넥션 종료"""
        if self._con is not None:
            try:
                self._con.close()
            except Exception:
                pass
            finally:
                self._con = None