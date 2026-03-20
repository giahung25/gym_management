import flet as ft
from gui import theme
from gui.components.header import Header
from gui.components.sidebar import Sidebar
from app.repositories import equipment_repo
from app.models.equipment import Equipment
from app.services import equipment_svc


def EquipmentScreen(page: ft.Page) -> ft.Row:
    filter_status = {"value": None}
    selected_eq = {"obj": None}

    # ── Form fields ──────────────────────────────────────────────────────────
    f_name = ft.TextField(label="Tên thiết bị *", expand=True)
    f_category = ft.TextField(label="Loại thiết bị *", expand=True)
    f_qty = ft.TextField(label="Số lượng", expand=True, keyboard_type=ft.KeyboardType.NUMBER, value="1")
    f_status = ft.Dropdown(
        label="Trạng thái",
        options=[
            ft.dropdown.Option(Equipment.STATUS_WORKING, "Hoạt động"),
            ft.dropdown.Option(Equipment.STATUS_BROKEN, "Hỏng"),
            ft.dropdown.Option(Equipment.STATUS_MAINTENANCE, "Bảo trì"),
        ],
        value=Equipment.STATUS_WORKING,
        expand=True,
    )
    f_purchase = ft.TextField(label="Ngày mua (YYYY-MM-DD)", expand=True)
    f_location = ft.TextField(label="Vị trí", expand=True)
    f_notes = ft.TextField(label="Ghi chú", expand=True, multiline=True, min_lines=2)
    dlg_error = ft.Text("", color=theme.RED, size=theme.FONT_SM)
    dlg_title = ft.Text("", size=theme.FONT_LG, weight=ft.FontWeight.BOLD)

    def save_eq(e):
        try:
            qty = int(f_qty.value or 1)
            if selected_eq["obj"] is None:
                equipment_svc.add_equipment(
                    name=f_name.value,
                    category=f_category.value,
                    quantity=qty,
                    purchase_date=f_purchase.value.strip() or None,
                    notes=f_notes.value.strip() or None,
                    location=f_location.value.strip() or None,
                )
            else:
                eq = selected_eq["obj"]
                equipment_svc.update_equipment(
                    eq,
                    name=f_name.value.strip(),
                    category=f_category.value.strip(),
                    quantity=qty,
                    status=f_status.value,
                    purchase_date=f_purchase.value.strip() or None,
                    location=f_location.value.strip() or None,
                    notes=f_notes.value.strip() or None,
                )
            eq_dialog.open = False
            page.update()
            refresh_table()
        except (ValueError, TypeError) as ex:
            dlg_error.value = str(ex)
            page.update()

    eq_dialog = ft.AlertDialog(
        modal=True,
        title=dlg_title,
        content=ft.Column(
            controls=[
                ft.Row(controls=[f_name, f_category], spacing=theme.PAD_MD),
                ft.Row(controls=[f_qty, f_status], spacing=theme.PAD_MD),
                ft.Row(controls=[f_purchase, f_location], spacing=theme.PAD_MD),
                f_notes,
                dlg_error,
            ],
            spacing=theme.PAD_MD, width=560, tight=True,
        ),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: setattr(eq_dialog, "open", False) or page.update()),
            ft.ElevatedButton("Lưu", on_click=save_eq, bgcolor=theme.ORANGE, color=theme.WHITE),
        ],
    )

    def open_add(e):
        selected_eq["obj"] = None
        for field in [f_name, f_category, f_purchase, f_location, f_notes]:
            field.value = ""
        f_qty.value = "1"
        f_status.value = Equipment.STATUS_WORKING
        dlg_error.value = ""
        dlg_title.value = "Thêm thiết bị mới"
        eq_dialog.open = True
        page.update()

    def open_edit(eq):
        selected_eq["obj"] = eq
        f_name.value = eq.name
        f_category.value = eq.category
        f_qty.value = str(eq.quantity)
        f_status.value = eq.status
        f_purchase.value = str(eq.purchase_date) if eq.purchase_date else ""
        f_location.value = getattr(eq, "location", "") or ""
        f_notes.value = eq.notes or ""
        dlg_error.value = ""
        dlg_title.value = "Chỉnh sửa thiết bị"
        eq_dialog.open = True
        page.update()

    delete_id = {"id": None}
    confirm_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Xác nhận xóa thiết bị"),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: setattr(confirm_dlg, "open", False) or page.update()),
            ft.ElevatedButton("Xóa", bgcolor=theme.RED, color=theme.WHITE,
                              on_click=lambda e: [equipment_repo.delete(delete_id["id"]),
                                                  setattr(confirm_dlg, "open", False),
                                                  page.update(), refresh_table()]),
        ],
    )

    STATUS_COLORS = {
        Equipment.STATUS_WORKING: (theme.GREEN_LIGHT, theme.GREEN, "Hoạt động"),
        Equipment.STATUS_BROKEN: (theme.RED_LIGHT, theme.RED, "Hỏng"),
        Equipment.STATUS_MAINTENANCE: (theme.AMBER_LIGHT, theme.AMBER, "Bảo trì"),
    }

    table_body = ft.Column(controls=[], spacing=0)
    summary_text = ft.Text("", size=theme.FONT_SM, color=theme.GRAY)

    def refresh_table():
        sv = filter_status["value"]
        equipments = equipment_repo.get_by_status(sv) if sv else equipment_repo.get_all()
        rows = []
        for eq in equipments:
            bg, fg, label = STATUS_COLORS.get(eq.status, (theme.GRAY_LIGHT, theme.GRAY, eq.status))
            rows.append(ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(eq.name, size=theme.FONT_SM, weight=ft.FontWeight.W_500,
                                color=theme.TEXT_PRIMARY, expand=True),
                        ft.Text(eq.category, size=theme.FONT_SM, color=theme.GRAY, width=120),
                        ft.Text(str(eq.quantity), size=theme.FONT_SM, color=theme.TEXT_PRIMARY, width=60),
                        ft.Container(
                            content=ft.Text(label, size=theme.FONT_XS, color=fg, weight=ft.FontWeight.W_600),
                            bgcolor=bg, border_radius=theme.BADGE_RADIUS,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3), width=90,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text(str(eq.purchase_date or "—"), size=theme.FONT_SM, color=theme.GRAY, width=110),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text("Sửa", size=theme.FONT_XS, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                                    border=ft.border.all(1, theme.ORANGE), border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    on_click=lambda e, item=eq: open_edit(item),
                                ),
                                ft.Container(
                                    content=ft.Text("Xóa", size=theme.FONT_XS, color=theme.RED, weight=ft.FontWeight.W_600),
                                    border=ft.border.all(1, theme.RED), border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    on_click=lambda e, item=eq: [
                                        delete_id.update({"id": item.id}),
                                        setattr(confirm_dlg, "open", True),
                                        page.update(),
                                    ],
                                ),
                            ],
                            spacing=theme.PAD_SM,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_MD),
                border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
            ))
        table_body.controls = rows
        summary = equipment_svc.get_equipment_summary()
        summary_text.value = (
            f"Tổng: {summary['total']}  |  "
            f"Hoạt động: {summary['working']}  |  "
            f"Bảo trì: {summary['maintenance']}  |  "
            f"Hỏng: {summary['broken']}"
        )
        page.update()

    filter_buttons_row = ft.Row(
        controls=[
            ft.ElevatedButton("Tất cả", on_click=lambda e: _set_filter(None),
                              bgcolor=theme.ORANGE, color=theme.WHITE),
            ft.OutlinedButton("Hoạt động", on_click=lambda e: _set_filter(Equipment.STATUS_WORKING)),
            ft.OutlinedButton("Bảo trì", on_click=lambda e: _set_filter(Equipment.STATUS_MAINTENANCE)),
            ft.OutlinedButton("Hỏng", on_click=lambda e: _set_filter(Equipment.STATUS_BROKEN)),
        ],
        spacing=theme.PAD_SM,
    )

    def _set_filter(val):
        filter_status["value"] = val
        refresh_table()

    col_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Tên thiết bị", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, expand=True),
                ft.Text("Loại", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=120),
                ft.Text("SL", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=60),
                ft.Text("Trạng thái", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=90),
                ft.Text("Ngày mua", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=110),
                ft.Text("Hành động", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=120),
            ],
        ),
        bgcolor=theme.BG,
        padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_SM),
    )

    page.overlay.extend([eq_dialog, confirm_dlg])

    main_content = ft.Column(
        controls=[
            Header(page),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Thiết bị", size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                                ft.ElevatedButton("+ Thêm thiết bị", bgcolor=theme.ORANGE, color=theme.WHITE, on_click=open_add),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        summary_text,
                        filter_buttons_row,
                        ft.Container(
                            content=ft.Column(controls=[col_header, table_body], spacing=0),
                            bgcolor=theme.CARD_BG,
                            border_radius=theme.CARD_RADIUS,
                            shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
                        ),
                    ],
                    spacing=theme.PAD_LG,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.all(theme.PAD_2XL),
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )

    refresh_table()

    return ft.Row(
        controls=[Sidebar(page, active_route="equipment"), main_content],
        spacing=0,
        expand=True,
    )
