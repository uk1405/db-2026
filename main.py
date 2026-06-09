from abc import ABC, abstractmethod
import pandas as pd

# 8.1 NBA 구단 테이블 인터페이스
class ITeamMasterRepository(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame):
        """ 새로운 NBA 구단 정보 등록 (CREATE) """
        pass

    @abstractmethod
    def find_all(self) -> pd.DataFrame:
        """ 전체 NBA 구단 목록 조회 (READ) """
        pass

    @abstractmethod
    def find_by_code(self, team_code: str) -> pd.DataFrame:
        """ 단일 구단 상세 정보 조회 (READ) """
        pass

    @abstractmethod
    def update(self, df: pd.DataFrame):
        """ 구단 정보 및 연고지 업데이트 (UPDATE) """
        pass

    @abstractmethod
    def delete_by_code(self, team_code: str) -> bool:
        """ 구단 삭제 처리 (DELETE) """
        pass


# 8.2 리그 등록 선수 테이블 인터페이스
class IPlayerRepository(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame):
        """ 신규 선수 프로필 추가 (CREATE) """
        pass

    @abstractmethod
    def find_all_players(self) -> pd.DataFrame:
        """ 리그 전체 선수 목록 조회 (READ) """
        pass

    @abstractmethod
    def update(self, df: pd.DataFrame):
        """ 선수 이름 및 포지션, 데뷔년도 수정 (UPDATE) """
        pass

    @abstractmethod
    def delete_by_id(self, player_id: str) -> bool:
        """ 선수 정보 삭제 (DELETE) """
        pass


# 8.3 계약 및 핵심 성적 스탯 테이블 인터페이스
class IContractStatRepository(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame):
        """ 새로운 구단 계약 및 스탯 등록 (CREATE) """
        pass

    @abstractmethod
    def find_by_team(self, team_code: str) -> pd.DataFrame:
        """ 특정 구단의 계약 정보 전체 조회 (READ) """
        pass

    @abstractmethod
    def update_contract(self, player_id: str, team_code: str, ppg: float, salary: int):
        """ 계약 연봉 및 경기당 평균 득점 갱신 (UPDATE) """
        pass


# 8.4 복합 Join 정보 인터페이스 (과제 필수 조건)
class IComplexJoinRepository(ABC):
    @abstractmethod
    def execute_roster_left_join(self, team_code: str) -> pd.DataFrame:
        """
        nba_team_master, nba_player, nba_contract_stat 3개 테이블을 Join하여
        특정 구단의 상세 정보와 소속 선수들의 성적/연봉 명단을 한 번에 조회
        """
        pass
