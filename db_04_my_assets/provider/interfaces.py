from abc import ABC, abstractmethod
import pandas as pd


class IAssetListProvider(ABC):
    @abstractmethod
    def fetch_asset_list(self) -> pd.DataFrame: ...

class IAssetPriceProvider(ABC):
    @abstractmethod
    def fetch_price_data(self, ticker: str, start_date: str) -> pd.DataFrame: ...
