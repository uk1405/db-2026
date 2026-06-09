from datetime import datetime, timedelta
import pandas as pd

from repository.interfaces import (
    IAssetRepository,
    IAccountRepository,
    IHoldingRepository,
    IDailyPriceRepository,
    IJoinRepository
)

from provider.interfaces import IAssetListProvider, IAssetPriceProvider


class FinanceService:

    def __init__(
        self,
        asset_repo: IAssetRepository,
        account_repo: IAccountRepository,
        holding_repo: IHoldingRepository,
        price_repo: IDailyPriceRepository,
        join_repo: IJoinRepository,
        
        asset_provider: IAssetListProvider,
        price_provider: IAssetPriceProvider
    ):
        """생성자 DI를 적용하여 Repository 및 Provider 주입"""
        self.asset_repo = asset_repo
        self.account_repo = account_repo
        self.holding_repo = holding_repo
        self.price_repo = price_repo
        self.join_repo = join_repo
        
        self.asset_provider = asset_provider
        self.price_provider = price_provider

    # =========================================================================
    # UC-01: 시스템 초기화 및 데이터 연동
    # =========================================================================
    def initialize(self) -> None:
        """테이블 생성"""
        print('[INFO] 데이터베이스 테이블 초기화 시작')
        self.asset_repo.create_table()
        self.account_repo.create_table()
        self.holding_repo.create_table()
        self.price_repo.create_table()

        self.add_all_assets()
        self.add_all_accounts()
        self.add_all_holdings()
        self.add_all_prices()
        print('[INFO] 데이터베이스 테이블 초기화 완료\n')

    def add_all_assets(self):
        """
        asset 데이터가 없다면 Provider를 통해 asset 데이터 삽입
        """
        count = self.asset_repo.count()
        if count == 0:
            print('[INFO] Provider를 통해 asset 데이터 삽입 시작')
            df_assets = self.asset_provider.fetch_asset_list()
            self.asset_repo.save(df_assets)
            print('[INFO] Provider를 통해 asset 데이터 삽입 완료')
        else:
            print(f'[INFO] asset 데이터: {count}개')

    def add_all_accounts(self):
        """
        account 데이터가 없다면 account 데이터 삽입
        """
        count = self.account_repo.count()
        if count == 0:
            print('[INFO] account 데이터 삽입 시작')
            df_accounts = pd.DataFrame([
                {"account_id": 1, "account_name": "ISA", "brokerage": "키움증권"},
                {"account_id": 2, "account_name": "연금저축펀드", "brokerage": "삼성증권"},
                {"account_id": 3, "account_name": "위탁계좌", "brokerage": "미래에셋"},
            ])
            self.account_repo.save(df_accounts)
            print('[INFO] account 데이터 삽입 완료')
        else:
            print(f'[INFO] account 데이터: {count}개')
    
    def add_all_holdings(self):
        """
        holding 데이터가 없다면 holding 데이터 삽입
        """
        count = self.holding_repo.count()
        if count == 0:
            print('[INFO] holding 데이터 삽입 시작')
            df_holdings = pd.DataFrame([
                {"ticker": "005930", "account_id": 3, "quantity": 1, "avg_buy_price": 200000},
                {"ticker": "0162Z0", "account_id": 2, "quantity": 10, "avg_buy_price": 13500},
                {"ticker": "360750", "account_id": 1, "quantity": 5, "avg_buy_price": 27000},
                {"ticker": "379810", "account_id": 1, "quantity": 5, "avg_buy_price": 29415},
            ])
            self.holding_repo.save(df_holdings)
            print('[INFO] holding 데이터 삽입 완료')
        else:
            print(f'[INFO] holding 데이터: {count}개')

    def add_all_prices(self) -> None:
        """
        최신 시세 데이터를 Provider를 통해 daily_price 테이블에 삽입
        """
        # 직전 영업일 계산
        today = pd.Timestamp.today()
        last_business_day = (today - pd.offsets.BDay(0 if today.dayofweek < 5 else 1)).date()

        # 가장 최신 price 날짜 확인
        latest_date = self.price_repo.find_latest_date()
        yesterday = last_business_day - timedelta(days=1)
        print(f"[INFO] price 저장 최신 날짜: {latest_date}, 직전 영업일: {yesterday}")

        # 데이터가 None이거나, 직전 영업일보다 과거라면 동기화 시작
        if not latest_date or latest_date < yesterday:
            one_year_ago = (last_business_day - pd.DateOffset(years=1)).date()

            # 시작 날짜 (None이면 1년 전, 값이 있으면 latest_date 다음날부터)
            start_date = one_year_ago if not latest_date else latest_date + timedelta(days=1)

            print(f"[INFO] {start_date}부터 {yesterday}까지의 시세 데이터 수집 시작")
            
            # 현재 보유 중인 티커 목록 조회
            holdings_df = self.holding_repo.find_all()
            if holdings_df.empty or "ticker" not in holdings_df.columns:
                print("[INFO] 현재 보유 중인 자산(Holding)이 없어 시세 데이터 수집 중단")
                return
                
            tickers = holdings_df["ticker"].unique()
            for ticker in tickers:
                df_prices = self.price_provider.fetch_price_data(ticker, start_date)
                self.price_repo.save(ticker, df_prices)

            print("[INFO] 전체 종목 시세 데이터 수집 완료")
        else:
            print(f"[INFO] 최신 시세 데이터 확인 완료 (최신 날짜: {latest_date})")

    # =========================================================================
    # UC-02: 종목 필터링 및 UC-03: 종목 필터링
    # =========================================================================
    def get_assets(self, keyword: str = None) -> pd.DataFrame:
        return self.asset_repo.find_by_keyword(keyword)

    # =========================================================================
    # UC-04: 계좌 목록 조회
    # =========================================================================
    def get_accounts(self) -> pd.DataFrame:
        return self.account_repo.find_all()

    # =========================================================================
    # UC-05: 자산 보유 현황 조회
    # =========================================================================
    def get_holdings(self) -> pd.DataFrame:
        return self.holding_repo.find_all()

    # =========================================================================
    # UC-06: 종목 시세 조회
    # =========================================================================
    def get_prices(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """
        ticker의 최근 1년간 시세 데이터를 DB로부터 얻어옴
        """
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        if not start_date:
            current_year = int(end_date[:4])
            start_date = f"{current_year - 1}-01-01"
            
        print(f"[INFO] {ticker}의 {start_date} ~ {end_date} 시세 데이터 조회 시작")
        return self.price_repo.find_by_date(ticker, start_date, end_date)

    # =========================================================================
    # UC-07: 종합 정보 조회 (Join 뷰)
    # =========================================================================
    def get_joined_dashboard_data(self) -> pd.DataFrame:
        """
        자산(Asset)-계좌(Account)-보유(Holding) 테이블 Join
        """
        return self.join_repo.find_all()