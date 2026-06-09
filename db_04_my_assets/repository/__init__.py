import os
from dotenv import load_dotenv


# 환경 변수에서 DB_TYPE 읽기 (기본값: DUCKDB)
load_dotenv()
DB_TYPE = os.getenv("DB_TYPE", "DUCKDB").upper()


# =========================================================================
# DB_TYPE에 따른 실제 구현체 매핑
# =========================================================================

if DB_TYPE == "DUCKDB":
    from .duckdb.connection import DuckDBManager as DatabaseManager
    from .duckdb.asset import DuckDBAssetRepository as AssetRepository
    from .duckdb.account import DuckDBAccountRepository as AccountRepository
    from .duckdb.holding import DuckDBHoldingRepository as HoldingRepository
    from .duckdb.price import DuckDBDailyPriceRepository as DailyPriceRepository
    from .duckdb.join import DuckDBJoinRepository as JoinRepository

elif DB_TYPE == "MYSQL":
    from .mysql.connection import MySQLManager as DatabaseManager
    from .mysql.asset import MySQLAssetRepository as AssetRepository
    from .mysql.account import MySQLAccountRepository as AccountRepository
    from .mysql.holding import MySQLHoldingRepository as HoldingRepository
    from .mysql.price import MySQLDailyPriceRepository as DailyPriceRepository
    from .mysql.join import MySQLJoinRepository as JoinRepository

elif DB_TYPE == "ORACLE":
    from .oracle.connection import OracleManager as DatabaseManager
    from .oracle.asset import OracleAssetRepository as AssetRepository
    from .oracle.account import OracleAccountRepository as AccountRepository
    from .oracle.holding import OracleHoldingRepository as HoldingRepository
    from .oracle.price import OracleDailyPriceRepository as DailyPriceRepository
    from .oracle.join import OracleJoinRepository as JoinRepository

elif DB_TYPE == "SUPABASE":
    from .supabase.connection import SupabaseManager as DatabaseManager
    from .supabase.asset import SupabaseAssetRepository as AssetRepository
    from .supabase.account import SupabaseAccountRepository as AccountRepository
    from .supabase.holding import SupabaseHoldingRepository as HoldingRepository
    from .supabase.price import SupabaseDailyPriceRepository as DailyPriceRepository
    from .supabase.join import SupabaseJoinRepository as JoinRepository

else:
    raise ValueError(f"지원하지 않는 DB_TYPE 설정입니다: {DB_TYPE}")

# =========================================================================
# 활성화된 DB 환경 정보 출력
# =========================================================================
print(f"[INFO] Database: {DB_TYPE}")

# =========================================================================
# 패키지 외부 노출
# =========================================================================
__all__ = [
    "DatabaseManager",
    "AssetRepository",
    "AccountRepository",
    "HoldingRepository",
    "DailyPriceRepository",
    "JoinRepository",
]