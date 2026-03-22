# ============================================================================
# FILE: gui/components/header.py
# MỤC ĐÍCH: Component HEADER — thanh trên cùng của mỗi màn hình (trừ Login).
#            Chứa: thanh tìm kiếm, nút thông báo, thông tin user.
#
# CÁCH DÙNG:
#   from gui.components.header import Header
#   header = Header(page)  # Tạo header → trả về ft.Container
#
# COMPONENT LÀ GÌ?
#   - Một phần giao diện có thể TÁI SỬ DỤNG nhiều nơi
#   - Header được dùng ở: Dashboard, Members, Memberships, Equipment, Reports
#   - Viết 1 lần, dùng nhiều lần → tránh lặp code
# ============================================================================

import flet as ft        # Framework GUI
from gui import theme    # Hằng số thiết kế (màu sắc, font size, spacing...)


def Header(page: ft.Page) -> ft.Container:
    """Tạo component Header — thanh trên cùng của ứng dụng.

    Tham số:
        page (ft.Page): đối tượng Page — dùng để gọi callback tìm kiếm

    Trả về:
        ft.Container: widget header đã sẵn sàng hiển thị

    Cấu trúc bên trong:
    ┌──────────────────────────────────────────────────────────────┐
    │  [🔍 Search members, packages...]     [🔔]  [👤 Admin User] │
    └──────────────────────────────────────────────────────────────┘
    """

    # ── Callback tìm kiếm ────────────────────────────────────────────────────
    def _on_search(e):
        """Được gọi mỗi khi user gõ vào ô tìm kiếm.

        Kiểm tra xem page có thuộc tính on_search_change không:
        - Nếu CÓ (screen đăng ký callback) → gọi callback với giá trị search
        - Nếu KHÔNG → bỏ qua (một số screen không cần tìm kiếm)

        getattr(obj, "attr", None): lấy thuộc tính, nếu không có → trả None
        callable(cb): kiểm tra cb có phải hàm (gọi được) không
        """
        cb = getattr(page, "on_search_change", None)  # Lấy callback (nếu có)
        if callable(cb):      # Nếu callback tồn tại và là hàm
            cb(e.control.value)  # Gọi callback, truyền giá trị ô search

    # ── Thanh tìm kiếm (Search Bar) ──────────────────────────────────────────
    search_bar = ft.Container(
        content=ft.Row(
            controls=[
                # Icon kính lúp
                ft.Icon(ft.Icons.SEARCH, color=theme.GRAY, size=16),
                # Ô nhập text tìm kiếm
                ft.TextField(
                    hint_text="Search members, packages...",  # Placeholder text
                    hint_style=ft.TextStyle(color=theme.GRAY, size=theme.FONT_SM),
                    border=ft.InputBorder.NONE,    # Không viền (viền do Container bọc ngoài)
                    height=36,
                    text_size=theme.FONT_SM,
                    content_padding=ft.padding.symmetric(horizontal=4, vertical=0),
                    expand=True,        # Chiếm hết chiều ngang còn lại trong Row
                    on_change=_on_search,  # Gọi _on_search mỗi khi user gõ
                ),
            ],
            spacing=theme.PAD_SM,  # Khoảng cách giữa icon và TextField
        ),
        bgcolor=theme.WHITE,                          # Nền trắng
        border_radius=theme.BUTTON_RADIUS,             # Bo góc 8px
        border=ft.border.all(1, theme.BORDER),         # Viền xám 1px
        padding=ft.padding.symmetric(horizontal=theme.PAD_MD, vertical=0),
        width=320,   # Chiều rộng cố định 320px
        height=40,   # Chiều cao 40px
    )

    # ── Nút thông báo (Notification Button) ──────────────────────────────────
    notification_btn = ft.Container(
        content=ft.Stack(
            # ft.Stack = xếp chồng các widget lên nhau (overlay)
            controls=[
                # Icon chuông thông báo
                ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color=theme.GRAY, size=22),
                # Chấm tròn cam nhỏ (badge) — thông báo chưa đọc
                ft.Container(
                    width=8, height=8,
                    bgcolor=theme.ORANGE,   # Chấm cam
                    border_radius=4,         # Bo tròn (4 = bán kính = 8/2 → hình tròn)
                    top=0, right=0,          # Đặt ở góc trên-phải của Stack
                ),
            ],
            width=24, height=24,
        ),
        width=40, height=40,
        bgcolor=theme.WHITE,
        border_radius=theme.BUTTON_RADIUS,
        border=ft.border.all(1, theme.BORDER),
        alignment=ft.Alignment.CENTER,  # Căn icon vào giữa container
    )

    # ── Avatar người dùng ─────────────────────────────────────────────────────
    user_avatar = ft.Container(
        content=ft.Text("A", color=theme.WHITE, size=theme.FONT_MD, weight=ft.FontWeight.BOLD),
        width=36, height=39,
        bgcolor=theme.ORANGE,       # Nền cam
        border_radius=18,            # Bo tròn (18 = gần bằng 36/2 → hình tròn)
        alignment=ft.Alignment.CENTER,
    )

    # ── Thông tin người dùng ──────────────────────────────────────────────────
    user_info = ft.Row(
        controls=[
            user_avatar,
            ft.Column(
                controls=[
                    ft.Text("Admin User", size=theme.FONT_SM, weight=ft.FontWeight.W_600,
                            color=theme.TEXT_PRIMARY),
                    ft.Text("Super Manager", size=theme.FONT_XS, color=theme.GRAY),
                ],
                spacing=0,      # Không khoảng cách giữa 2 dòng text
                tight=True,     # Column co lại vừa đúng nội dung
            ),
            # Mũi tên xuống (gợi ý có dropdown menu — chưa implement)
            ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN, color=theme.GRAY, size=16),
        ],
        spacing=theme.PAD_SM,
    )

    # ── Trả về Container header hoàn chỉnh ───────────────────────────────────
    return ft.Container(
        content=ft.Row(
            controls=[
                search_bar,  # Bên trái: ô tìm kiếm
                ft.Row(
                    controls=[notification_btn, user_info],  # Bên phải: thông báo + user
                    spacing=theme.PAD_MD,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,        # Hai bên cách xa nhau
            vertical_alignment=ft.CrossAxisAlignment.CENTER,      # Căn giữa theo chiều dọc
        ),
        height=theme.HEADER_HEIGHT,   # Chiều cao cố định 64px
        bgcolor=theme.WHITE,           # Nền trắng
        padding=ft.padding.symmetric(horizontal=theme.PAD_2XL, vertical=theme.PAD_MD),
        border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),  # Viền dưới
    )
