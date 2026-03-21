import flet as ft
from gui import theme
from app.core.security import check_login


def LoginScreen(page: ft.Page) -> ft.Container:
    error_text = ft.Text("", color=theme.RED, size=theme.FONT_SM)
    username_field = ft.TextField(
        label="Tên đăng nhập",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=theme.BUTTON_RADIUS,
        focused_border_color=theme.ORANGE,
    )
    password_field = ft.TextField(
        label="Mật khẩu",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        border_radius=theme.BUTTON_RADIUS,
        focused_border_color=theme.ORANGE,
    )

    def do_login(e):
        error_text.value = ""
        if not username_field.value or not password_field.value:
            error_text.value = "Vui lòng nhập đầy đủ thông tin."
            page.update()
            return
        if check_login(username_field.value, password_field.value):
            page.navigate("dashboard")
        else:
            error_text.value = "Tên đăng nhập hoặc mật khẩu không đúng."
            password_field.value = ""
            page.update()

    password_field.on_submit = do_login

    login_card = ft.Container(
        width=400,
        content=ft.Column(
            controls=[
                # Logo
                ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "G",
                                color=theme.WHITE,
                                size=36,
                                weight=ft.FontWeight.BOLD,
                            ),
                            width=64,
                            height=64,
                            bgcolor=theme.ORANGE,
                            border_radius=16,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text(
                            "GymAdmin",
                            size=theme.FONT_2XL,
                            weight=ft.FontWeight.BOLD,
                            color=theme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            "MANAGEMENT SYSTEM",
                            size=theme.FONT_XS,
                            color=theme.GRAY,
                            weight=ft.FontWeight.W_500,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=theme.PAD_SM,
                ),
                ft.Container(height=theme.PAD_LG),
                ft.Text(
                    "Đăng nhập",
                    size=theme.FONT_LG,
                    weight=ft.FontWeight.BOLD,
                    color=theme.TEXT_PRIMARY,
                ),
                ft.Container(height=theme.PAD_XS),
                username_field,
                password_field,
                error_text,
                ft.Container(height=theme.PAD_XS),
                ft.Container(
                    content=ft.Text(
                        "Đăng nhập",
                        color=theme.WHITE,
                        size=theme.FONT_MD,
                        weight=ft.FontWeight.W_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    bgcolor=theme.ORANGE,
                    border_radius=theme.BUTTON_RADIUS,
                    padding=ft.padding.symmetric(vertical=14),
                    alignment=ft.Alignment.CENTER,
                    on_click=do_login,
                    ink=True,
                ),
            ],
            spacing=theme.PAD_MD,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            tight=True,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=ft.padding.all(theme.PAD_2XL + theme.PAD_MD),
        shadow=ft.BoxShadow(blur_radius=24, color="#00000018", offset=ft.Offset(0, 4)),
    )

    return ft.Container(
        expand=True,
        bgcolor=theme.BG,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_CENTER,
            end=ft.Alignment.BOTTOM_CENTER,
            colors=["#FFF0E6", theme.BG],
            stops=[0.0, 0.4],
        ),
        # Căn giữa card cả ngang lẫn dọc bằng alignment
        alignment=ft.Alignment.CENTER,
        content=login_card,
    )
