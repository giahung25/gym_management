import flet as ft
from gui import theme


def Header(page: ft.Page) -> ft.Container:
    def _on_search(e):
        cb = getattr(page, "on_search_change", None)
        if callable(cb):
            cb(e.control.value)

    search_bar = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.SEARCH, color=theme.GRAY, size=16),
                ft.TextField(
                    hint_text="Search members, packages...",
                    hint_style=ft.TextStyle(color=theme.GRAY, size=theme.FONT_SM),
                    border=ft.InputBorder.NONE,
                    height=36,
                    text_size=theme.FONT_SM,
                    content_padding=ft.padding.symmetric(horizontal=4, vertical=0),
                    expand=True,
                    on_change=_on_search,
                ),
            ],
            spacing=theme.PAD_SM,
        ),
        bgcolor=theme.WHITE,
        border_radius=theme.BUTTON_RADIUS,
        border=ft.border.all(1, theme.BORDER),
        padding=ft.padding.symmetric(horizontal=theme.PAD_MD, vertical=0),
        width=320,
        height=40,
    )

    notification_btn = ft.Container(
        content=ft.Stack(
            controls=[
                ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color=theme.GRAY, size=22),
                ft.Container(
                    width=8,
                    height=8,
                    bgcolor=theme.ORANGE,
                    border_radius=4,
                    top=0,
                    right=0,
                ),
            ],
            width=24,
            height=24,
        ),
        width=40,
        height=40,
        bgcolor=theme.WHITE,
        border_radius=theme.BUTTON_RADIUS,
        border=ft.border.all(1, theme.BORDER),
        alignment=ft.Alignment.CENTER,
    )

    user_avatar = ft.Container(
        content=ft.Text("A", color=theme.WHITE, size=theme.FONT_MD, weight=ft.FontWeight.BOLD),
        width=36,
        height=39,
        bgcolor=theme.ORANGE,
        border_radius=18,
        alignment=ft.Alignment.CENTER,
    )

    user_info = ft.Row(
        controls=[
            user_avatar,
            ft.Column(
                controls=[
                    ft.Text("Admin User", size=theme.FONT_SM, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                    ft.Text("Super Manager", size=theme.FONT_XS, color=theme.GRAY),
                ],
                spacing=0,
                tight=True,
            ),
            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.GRAY, size=16),
        ],
        spacing=theme.PAD_SM,
    )

    return ft.Container(
        content=ft.Row(
            controls=[
                search_bar,
                ft.Row(
                    controls=[notification_btn, user_info],
                    spacing=theme.PAD_MD,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=theme.HEADER_HEIGHT,
        bgcolor=theme.WHITE,
        padding=ft.padding.symmetric(horizontal=theme.PAD_2XL, vertical=theme.PAD_MD),
        border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
    )
