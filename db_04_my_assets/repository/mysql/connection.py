import os
import pymysql
from dotenv import load_dotenv
from ..interfaces import IDatabaseManager

# 환경 변수 로드
load_dotenv()


class MySQLManager(IDatabaseManager):
    """MySQL 커넥션 관리 클래스"""

    def __init__(self):
        # .env에서 MySQL 접속 정보 로드
        host = os.getenv("MYSQL_HOST", "localhost")
        port = int(os.getenv("MYSQL_PORT", 3306))
        user = os.getenv("MYSQL_USER", "root")
        password = os.getenv("MYSQL_PASSWORD", "password")
        database = os.getenv("MYSQL_DB", "finance")

        try:
            self._con = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
        except pymysql.err.OperationalError as e:
            # Database가 없다면 database없이 접속 후 생성
            if e.args[0] == pymysql.constants.ER.BAD_DB_ERROR: # 1049
                self._con = pymysql.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password,
                    # database=database,
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True
                )

                with self._con.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
                    cursor.execute(f"USE {database}")
            else:
                raise e

    def get_connection(self) -> pymysql.connections.Connection:
        """
        현재 활성화된 MySQL 커넥션 반환
        기존 연결이 없다면 새로 연결을 맺고, 있다면 기존 객체 재사용
        """
        # # 연결이 없거나, 연결이 끊어졌는지 확인 (ping() 메서드 활용)
        # if self._con is None:
        #     self._create_new_connection()
        # else:
        #     self._create_new_connection()

        return self._con

    def _create_new_connection(self) -> None:
        """MySQL 서버와 연결"""
        try:
            self._con = pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                password=self._password,
                database=self._db,
                charset="utf8mb4",
                # 조회 결과를 튜플 형태가 아닌 딕셔너리 형태로 받음
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            raise ConnectionError(
                f"[ERROR] MySQL 연결 실패 (Host: {self._host}:{self._port}, DB: {self._db}): {e}"
            )

    def close(self) -> None:
        """현재 열려 있는 MySQL 커넥션 종료"""
        if self._con is not None:
            try:
                self._con.close()
            except Exception:
                pass
            finally:
                self._con = None