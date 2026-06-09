import flet as ft
import duckdb
import pandas as pd
import data_source as data
import repository as repo


# =========================================================================
# region: Service (Business Logic)
# =========================================================================
def add_all_assets(con: duckdb.DuckDBPyConnection):
    count = repo.get_assets_count(con)
    if count <= 0:
        df = data.fetch_asset_list()
        repo.save_assets(con, df)
    else:
        print(f"[INFO] 종목 데이터 개수: {count}")

# endregion


# =========================================================================
# region: Main
# =========================================================================
def main(page: ft.Page):
    # region [Page Setup]
    page.title = "Finance Database"
    page.padding = 16
    page.window.width = 700
    page.window.height = 500
    page.theme_mode = ft.ThemeMode.DARK  # 깔끔한 다크모드 추가
    # endregion

    con = duckdb.connect("data/finance.db")

    repo.create_table(con)
    add_all_assets(con)

    # 초기 전체 종목 리스트 로드
    df = repo.find_assets_by_keyword(con, None)

    # DataTable 행 생성 헬퍼 함수
    def create_rows(df) -> list:
        return [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(value))) 
                    for value in row
                ]
            ) for row in df.values
        ]

    # 주식 목록을 보여줄 데이터 테이블
    table_assets = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(str.upper(col))) 
            for col in df.columns
        ],
        rows=create_rows(df),
    )

    # Filtering (엔터 입력 시 필터링 수행)
    def on_filter_change(e):
        # 입력된 텍스트로 asset 테이블 검색
        filtered_df = repo.find_assets_by_keyword(con, e.control.value)

        # 기존 테이블 초기화 후 필터링된 데이터 반영
        table_assets.rows.clear()
        table_assets.rows = create_rows(filtered_df)

        page.update()

    filter_input = ft.Container(
        content=ft.TextField(
            label="종목 검색",
            prefix_icon=ft.Icons.SEARCH,
            hint_text="종목명 또는 티커를 입력하고 엔터를 치세요",
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            margin=16,
            expand=True,
            on_submit=on_filter_change,  # 엔터 치면 검색 함수 실행
        )
    )

    # 종목 탭 내용 레이아웃 (스크롤 기능 포함)
    tab_assets = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.ALWAYS,
        controls=[filter_input, table_assets],
    )

    # 기타 임시 탭 텍스트 설정
    tab_accounts = ft.Container(content=ft.Text("계좌 목록 화면입니다."), padding=20)
    tab_holdings = ft.Container(content=ft.Text("보유 자산 화면입니다."), padding=20)
    tab_prices = ft.Container(content=ft.Text("일별 시세 화면입니다."), padding=20)
    tab_join = ft.Container(content=ft.Text("테이블 Join 화면입니다."), padding=20)

    # 상단 탭 컴포넌트 구성
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


if __name__ == "__main__":
    ft.run(main)

# endregion
