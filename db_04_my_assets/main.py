import flet as ft

from repository import (
    DatabaseManager,
    AssetRepository,
    AccountRepository,
    HoldingRepository,
    DailyPriceRepository,
    JoinRepository,
)
from provider import AssetListProvider, AssetPriceProvider
from service import FinanceService
import views


def main(page: ft.Page):
    # region [Page Setup]
    page.title = "My Assets"
    page.padding = 16
    page.window.width = 700
    page.window.height = 500
    # endregion

    # =========================================================================
    # region [의존성 주입 및 데이터베이스 초기화]
    # =========================================================================
    # .env의 DB_TYPE 설정에 맞는 DB 매니저가 자동으로 선택됨
    db_manager = DatabaseManager()

    # 각 레포지토리에 DB 매니저 주입
    asset_repo = AssetRepository(db_manager)
    account_repo = AccountRepository(db_manager)
    holding_repo = HoldingRepository(db_manager)
    price_repo = DailyPriceRepository(db_manager)
    join_repo = JoinRepository(db_manager)

    asset_provider = AssetListProvider()
    price_provider = AssetPriceProvider()

    # Service에 의존성 주입
    service = FinanceService(
        asset_repo=asset_repo,
        account_repo=account_repo,
        holding_repo=holding_repo,
        price_repo=price_repo,
        join_repo=join_repo,

        asset_provider=asset_provider,
        price_provider=price_provider
    )

    service.initialize()
    # endregion

    # =========================================================================
    # region [탭 뷰 생성]
    # =========================================================================
    # tab_assets = ft.Text("종목")
    # tab_accounts = ft.Text("계좌")
    # tab_holdings = ft.Text("보유")
    # tab_prices = ft.Text("시세")
    # tab_join = ft.Text("Join")

    assets_df = service.get_assets(None)

    def search_assets(keyword: str):
        return service.get_assets(keyword)

    tab_assets = views.create_asset_view(assets_df, search_assets)

    accounts_df = service.get_accounts()
    tab_accounts = views.create_account_view(accounts_df)

    holdings_df = service.get_holdings()
    tab_holdings = views.create_holding_view(holdings_df)

    join_df = service.get_joined_dashboard_data()
    tab_join = views.create_join_view(join_df)

    join_df = join_df.sort_values(by="quantity", ascending=False)
    tab_prices = views.create_price_view(service, join_df[["name", "ticker"]])
    # endregion

    # =========================================================================
    # region [Flet UI 레이아웃 구성]
    # =========================================================================
    tabs = ft.Tabs(
        length=5,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="종목", icon=ft.Icons.MONETIZATION_ON_OUTLINED),
                        ft.Tab(label="계좌", icon=ft.Icons.SAVINGS_OUTLINED),
                        ft.Tab(label="보유", icon=ft.Icons.FAVORITE_BORDER_OUTLINED),
                        ft.Tab(label="시세", icon=ft.Icons.CANDLESTICK_CHART_OUTLINED),
                        ft.Tab(label="Join", icon=ft.Icons.JOIN_LEFT_OUTLINED),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        tab_assets,
                        tab_accounts,
                        tab_holdings,
                        tab_prices,
                        tab_join,
                    ],
                ),
            ],
        ),
    )

    page.add(tabs)
    # endregion


if __name__ == "__main__":
    ft.run(main)