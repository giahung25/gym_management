import sys
import os

# Thêm thư mục gốc vào sys.path để tìm thấy module gui/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import flet as ft
from app.core.config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from app.core.database import init_db
from gui.dashboard import DashboardScreen


def main(page: ft.Page):
    # Khởi tạo DB — bắt lỗi để app không crash thầm lặng
    try:
        init_db()
    except Exception as e:
        print(f"[ERROR] Không thể khởi tạo database: {e}")
        raise

    page.title = APP_TITLE
    page.window_width = WINDOW_WIDTH
    page.window_height = WINDOW_HEIGHT
    page.bgcolor = "#F5F5F5"
    page.padding = 0

    def navigate(route: str):
        # Clear overlay trước để tránh dialogs tích lũy sau mỗi lần navigate
        page.overlay.clear()
        page.controls.clear()
        if route == "dashboard":
            page.add(DashboardScreen(page))
        elif route == "members":
            from gui.members import MembersScreen
            page.add(MembersScreen(page))
        elif route == "packages":
            from gui.memberships import MembershipsScreen
            page.add(MembershipsScreen(page))
        elif route == "equipment":
            from gui.equipment import EquipmentScreen
            page.add(EquipmentScreen(page))
        elif route == "reports":
            from gui.reports import ReportsScreen
            page.add(ReportsScreen(page))
        else:
            page.add(DashboardScreen(page))
        page.update()

    # Inject navigate vào page để Sidebar có thể dùng
    page.navigate = navigate

    navigate("dashboard")


ft.run(main)
