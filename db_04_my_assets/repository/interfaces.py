from abc import ABC, abstractmethod
import pandas as pd


# =========================================================================
# 데이터베이스 연결 인터페이스
# =========================================================================
class IDatabaseManager(ABC):
    """데이터베이스 연결 관리 인터페이스"""

    @abstractmethod
    def get_connection(self):
        """데이터베이스 커넥션 객체 반환"""
        ...

    @abstractmethod
    def close(self) -> None:
        """현재 활성화된 데이터베이스 커넥션 close"""
        ...
        
        
# =========================================================================
# 공통 레포지토리 인터페이스
# =========================================================================
class IRepository(ABC):
    """공통 인터페이스"""
    
    def __init__(self, db: IDatabaseManager):
        self._con = db.get_connection()

    @abstractmethod
    def create_table(self) -> None:
        """테이블 생성"""
        ...

    @abstractmethod
    def count(self) -> int:
        """테이블의 Cardinality 반환"""
        ...


# =========================================================================
# 각 테이블별 확장 인터페이스
# =========================================================================

class IAssetRepository(IRepository):
    @abstractmethod
    def save(self, df: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def find_by_keyword(self, keyword: str = None) -> pd.DataFrame:
        ...


class IAccountRepository(IRepository):
    @abstractmethod
    def save(self, df: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        ...


class IHoldingRepository(IRepository):
    @abstractmethod
    def save(self, df: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        ...


class IDailyPriceRepository(IRepository):
    @abstractmethod
    def find_latest_date(self) -> str:
        ...

    @abstractmethod
    def save(self, ticker: str, df: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def find_by_date(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        ...


class IJoinRepository(ABC):
    def __init__(self, db: IDatabaseManager):
        self.con = db.get_connection()

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        ...