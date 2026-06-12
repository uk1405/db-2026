import flet as ft
import pandas as pd  # 💡 pands -> pandas로 수정
import duckdb

def main(page: ft.Page):  # 💡 ft.page -> ft.Page로 수정 (대문자)
    page.title = "Asset List"  # 💡 Lise -> List로 수정
    page.padding = 16
    page.window.width = 400
    page.window.height = 400

    con = duckdb.connect("data/finance.db")

    con.execute("""
        CREATE TABLE IF NOT EXISTS assets(  
                ticker VARCHAR PRIMARY KEY,
                name VARCHAR,
                type VARCHAR
                )
    """)

    con.execute("""
           INSERT OR IGNORE INTO assets
            SELECT * from read_csv_auto("data/assets.csv")     
        """)
    
    print("데이터베이스 저장 완료")

    snack_bar = ft.SnackBar(
        content = ft.Text("데이터베이스 저장 완료")
    )
    page.overlay.append(snack_bar)
    snack_bar.open = True
    page.update()  # 💡 스낵바를 화면에 실제로 그리려면 새로고침이 필요합니다!

if __name__ == "__main__":  # 💡 if 소문자 수정 및 맨 뒤에 콜론(:) 추가!
    ft.run(main)
