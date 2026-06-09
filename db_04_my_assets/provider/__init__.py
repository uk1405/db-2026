import os
# from .interfaces import IAssetListProvider, IAssetPriceProvider

DATA_PROVIDER = os.getenv("DATA_PROVIDER", "FDR").upper()

if DATA_PROVIDER == "FDR":
    from .fdr.provider import FDRAssetListProvider, FDRAssetPriceProvider
    
    AssetListProvider = FDRAssetListProvider
    AssetPriceProvider = FDRAssetPriceProvider

elif DATA_PROVIDER == "PYKRX":
    from .pykrx.provider import PyKrxAssetListProvider, PyKrxAssetPriceProvider
    
    AssetListProvider = PyKrxAssetListProvider
    AssetPriceProvider = PyKrxAssetPriceProvider

elif DATA_PROVIDER == "YFINANCE":
    from .yfinance.provider import YFinanceAssetListProvider, YFinanceAssetPriceProvider
    
    AssetListProvider = YFinanceAssetListProvider
    AssetPriceProvider = YFinanceAssetPriceProvider

else:
    from .fdr.provider import FDRAssetListProvider, FDRAssetPriceProvider
    
    AssetListProvider = FDRAssetListProvider
    AssetPriceProvider = FDRAssetPriceProvider


__all__ = [
    "AssetListProvider",
    "AssetPriceProvider",
]