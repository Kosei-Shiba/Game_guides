import flet as ft
import controls

def main(page: ft.Page):
    # ページの設定
    page.title = "パワフェス　経験点計算"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    contents=controls.PawaCal()
    
    page.add(
        ft.Column(
            [contents,]
        )
    )

# アプリケーションの開始
ft.app(main)
