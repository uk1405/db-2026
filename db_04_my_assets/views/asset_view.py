import flet as ft
import flet_datatable2 as ftd

# import pandas as pd
# from typing import Callable


# def create_asset_view(
#     df: pd.DataFrame, 
#     on_search: Callable[[str], pd.DataFrame]
# ) -> ft.Control:
def create_asset_view(df, on_search) -> ft.Control:
    column_width = [
        {"fixed_width": 80},   # TICKER
        {"expand": True},      # NAME
        {"fixed_width": 100},  # TYPE
        {"fixed_width": 100}   # COUNTRY
    ]

    # DataTable2
    def create_rows(df) -> ftd.DataRow2:
        return [
            ftd.DataRow2(
                cells=[
                    ft.DataCell(ft.Text(str(value))) 
                    for value in row
                ]
            ) for row in df.values
        ]

    table_assets = ftd.DataTable2(
        expand=True,
        columns=[
            ftd.DataColumn2(
                label=ft.Text(str.upper(col)),
                **column_width[i]   # dict unpacking(**)으로 고정 너비 또는 확장 옵션 적용
            ) 
            for i, col in enumerate(df.columns)
        ],
        rows= create_rows(df),
    )

    def on_filter_change(e):
        keyword = e.control.value
        # main에서 넘겨받은 on_search()를 실행하여 필터링 결과 받아옴
        filtered_df = on_search(keyword)
        
        table_assets.rows.clear()
        table_assets.rows = create_rows(filtered_df)

        e.page.update()

    filter_input = ft.Container(
        ft.TextField(
            label="종목 검색",
            prefix_icon=ft.Icons.SEARCH,
            hint_text="종목명을 입력하세요",
            hint_style=ft.TextStyle(color=ft.Colors.GREY_700),
            margin=16,
            expand=True,
            on_submit=on_filter_change,
        )
    )

    return ft.Column(
        expand=True,
        controls=[filter_input, table_assets],
    )