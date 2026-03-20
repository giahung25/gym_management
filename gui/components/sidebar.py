import flet as ft
from gui import theme


def Sidebar(page: ft.Page, active_route: str = "dashboard") -> ft.Container:
    nav_icons = {
        "dashboard": ft.Icons.DASHBOARD_ROUNDED,
        "members": ft.Icons.PEOPLE_ALT_ROUNDED,
        "packages": ft.Icons.FITNESS_CENTER_ROUNDED,
        "equipment": ft.Icons.SETTINGS_ROUNDED,
        "reports": ft.Icons.BAR_CHART_ROUNDED,
    }

    nav_labels = {
        "dashboard": "Dashboard",
        "members": "Members",
        "packages": "Gym Packages",
        "equipment": "Equipment",
        "reports": "Reports",
    }

    navigate = getattr(page, "navigate", None)

    def make_nav_item(route: str) -> ft.Container:
        is_active = route == active_route
        label = nav_labels[route]

        def on_click(e, r=route):
            if navigate:
                navigate(r)

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        nav_icons[route],
                        size=18,
                        color=theme.WHITE if is_active else theme.GRAY,
                    ),
                    ft.Text(
                        label,
                        size=theme.FONT_SM,
                        weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
                        color=theme.WHITE if is_active else theme.GRAY,
                    ),
                ],
                spacing=theme.PAD_MD,
            ),
            bgcolor=theme.ORANGE if is_active else "transparent",
            border_radius=theme.BUTTON_RADIUS,
            padding=ft.padding.symmetric(horizontal=theme.PAD_MD, vertical=10),
            margin=ft.margin.symmetric(horizontal=theme.PAD_SM, vertical=2),
            on_click=on_click,
            ink=True,
        )

    nav_controls = [make_nav_item(r) for r in nav_icons]

    logo_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("P", color=theme.WHITE, size=20, weight=ft.FontWeight.BOLD),
                            width=36,
                            height=36,
                            bgcolor=theme.ORANGE,
                            border_radius=8,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("GymAdmin", color=theme.WHITE, size=theme.FONT_MD, weight=ft.FontWeight.BOLD),
                                ft.Text("MANAGEMENT SYSTEM", color=theme.GRAY, size=8, weight=ft.FontWeight.W_500),
                            ],
                            spacing=0,
                            tight=True,
                        ),
                    ],
                    spacing=theme.PAD_SM,
                ),
            ],
        ),
        padding=ft.padding.all(theme.PAD_XL),
    )

    add_member_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD, color=theme.WHITE, size=16),
                ft.Text("Add Member", color=theme.WHITE, size=theme.FONT_SM, weight=ft.FontWeight.W_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=theme.PAD_XS,
        ),
        bgcolor=theme.ORANGE,
        border_radius=theme.BUTTON_RADIUS,
        padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=10),
        margin=ft.margin.symmetric(horizontal=theme.PAD_MD, vertical=theme.PAD_MD),
        on_click=lambda e: navigate("members") if navigate else None,
        ink=True,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                logo_section,
                ft.Divider(color="#2D2D44", height=1, thickness=1),
                ft.Container(
                    content=ft.Column(controls=nav_controls, spacing=0),
                    padding=ft.padding.symmetric(vertical=theme.PAD_MD),
                    expand=True,
                ),
                add_member_btn,
            ],
            spacing=0,
            expand=True,
        ),
        width=theme.SIDEBAR_WIDTH,
        bgcolor=theme.SIDEBAR_BG,
        expand=False,
    )
