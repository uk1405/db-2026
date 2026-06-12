from abc import ABC, abstractmethod

class ITeamMasterRepository(ABC):
    @abstractmethod
    def find_all_teams(self) -> list:
        pass

    @abstractmethod
    def find_team_by_code(self, team_code: str) -> dict:
        pass


class IPlayerRepository(ABC):
    @abstractmethod
    def find_roster_by_team(self, team_code: str) -> list:
        pass

    @abstractmethod
    def save_player_transaction(self, player_data: dict, contract_data: dict) -> bool:
        pass
