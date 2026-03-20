import flet as ft
from gui import theme
from gui.components.header import Header
from gui.components.sidebar import Sidebar
from app.repositories import member_repo
from app.services import member_svc


def MembersScreen(page: ft.Page) -> ft.Row:
    # State
    search_query = {"value": ""}
    selected_member = {"obj": None}

    # ── Dialog: Add / Edit ──────────────────────────────────────────────────
    f_name = ft.TextField(label="Họ tên *", expand=True)
    f_phone = ft.TextField(label="Số điện thoại *", expand=True)
    f_email = ft.TextField(label="Email", expand=True)
    f_gender = ft.Dropdown(
        label="Giới tính",
        options=[
            ft.dropdown.Option("male", "Nam"),
            ft.dropdown.Option("female", "Nữ"),
            ft.dropdown.Option("other", "Khác"),
        ],
        expand=True,
    )
    f_dob = ft.TextField(label="Ngày sinh (YYYY-MM-DD)", expand=True)
    f_address = ft.TextField(label="Địa chỉ", expand=True)
    f_emergency = ft.TextField(label="Liên hệ khẩn cấp", expand=True)
    dialog_error = ft.Text("", color=theme.RED, size=theme.FONT_SM)
    dialog_title = ft.Text("", size=theme.FONT_LG, weight=ft.FontWeight.BOLD)

    def clear_form():
        for f in [f_name, f_phone, f_email, f_dob, f_address, f_emergency]:
            f.value = ""
        f_gender.value = None
        dialog_error.value = ""

    def save_member(e):
        try:
            if selected_member["obj"] is None:
                member_svc.register_member(
                    name=f_name.value,
                    phone=f_phone.value,
                    email=f_email.value or None,
                    gender=f_gender.value,
                    date_of_birth=f_dob.value or None,
                    address=f_address.value or None,
                    emergency_contact=f_emergency.value or None,
                )
            else:
                m = selected_member["obj"]
                m.name = f_name.value.strip()
                m.phone = f_phone.value.strip()
                m.email = f_email.value.strip() if f_email.value else None
                m.gender = f_gender.value
                m.date_of_birth = f_dob.value or None
                m.address = f_address.value or None
                m.emergency_contact = f_emergency.value or None
                member_svc.update_member(m)
            member_dialog.open = False
            page.update()
            refresh_table()
        except ValueError as ex:
            dialog_error.value = str(ex)
            page.update()

    member_dialog = ft.AlertDialog(
        modal=True,
        title=dialog_title,
        content=ft.Column(
            controls=[
                ft.Row(controls=[f_name, f_phone], spacing=theme.PAD_MD),
                ft.Row(controls=[f_email, f_gender], spacing=theme.PAD_MD),
                ft.Row(controls=[f_dob, f_emergency], spacing=theme.PAD_MD),
                f_address,
                dialog_error,
            ],
            spacing=theme.PAD_MD,
            width=560,
            tight=True,
        ),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: close_dialog()),
            ft.ElevatedButton("Lưu", on_click=save_member, bgcolor=theme.ORANGE, color=theme.WHITE),
        ],
    )

    def close_dialog():
        member_dialog.open = False
        page.update()

    def open_add_dialog(e):
        selected_member["obj"] = None
        clear_form()
        dialog_title.value = "Thêm hội viên mới"
        member_dialog.open = True
        page.update()

    def open_edit_dialog(m):
        selected_member["obj"] = m
        clear_form()
        dialog_title.value = "Chỉnh sửa hội viên"
        f_name.value = m.name
        f_phone.value = m.phone
        f_email.value = m.email or ""
        f_gender.value = m.gender
        f_dob.value = str(m.date_of_birth) if m.date_of_birth else ""
        f_address.value = m.address or ""
        f_emergency.value = m.emergency_contact or ""
        member_dialog.open = True
        page.update()

    # ── Confirm delete dialog ────────────────────────────────────────────────
    delete_target = {"id": None}

    def confirm_delete(m):
        delete_target["id"] = m.id
        confirm_dlg.content = ft.Text(f"Xóa hội viên '{m.name}'? Hành động này không thể hoàn tác.")
        confirm_dlg.open = True
        page.update()

    def do_delete(e):
        member_repo.delete(delete_target["id"])
        confirm_dlg.open = False
        page.update()
        refresh_table()

    confirm_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Xác nhận xóa"),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: setattr(confirm_dlg, "open", False) or page.update()),
            ft.ElevatedButton("Xóa", on_click=do_delete, bgcolor=theme.RED, color=theme.WHITE),
        ],
    )

    # ── Table ────────────────────────────────────────────────────────────────
    table_body = ft.Column(controls=[], spacing=0)

    def _make_row(m) -> ft.Container:
        initials = "".join(w[0].upper() for w in m.name.split()[:2])
        colors = ["#8B5CF6", "#3B82F6", "#EC4899", "#10B981", "#F59E0B"]
        avatar_color = colors[hash(m.id) % len(colors)]
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(initials, color=theme.WHITE, size=theme.FONT_SM, weight=ft.FontWeight.BOLD),
                                width=36, height=36, bgcolor=avatar_color,
                                border_radius=18, alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(m.name, size=theme.FONT_SM, weight=ft.FontWeight.W_500, color=theme.TEXT_PRIMARY),
                                    ft.Text(m.phone, size=theme.FONT_XS, color=theme.GRAY),
                                ],
                                spacing=0, tight=True,
                            ),
                        ],
                        spacing=theme.PAD_MD, expand=True,
                    ),
                    ft.Text(m.email or "—", size=theme.FONT_SM, color=theme.GRAY, width=180),
                    ft.Text(m.gender or "—", size=theme.FONT_SM, color=theme.GRAY, width=80),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text("Sửa", size=theme.FONT_XS, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                                border=ft.border.all(1, theme.ORANGE), border_radius=6,
                                padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                on_click=lambda e, member=m: open_edit_dialog(member),
                            ),
                            ft.Container(
                                content=ft.Text("Xóa", size=theme.FONT_XS, color=theme.RED, weight=ft.FontWeight.W_600),
                                border=ft.border.all(1, theme.RED), border_radius=6,
                                padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                on_click=lambda e, member=m: confirm_delete(member),
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
        )

    def refresh_table():
        kw = search_query["value"].strip()
        members = member_repo.search(kw) if kw else member_repo.get_all()
        table_body.controls = [_make_row(m) for m in members]
        stats = member_svc.get_member_stats()
        total_text.value = f"Tổng: {stats['total']} | Active: {stats['active']} | Mới tháng này: {stats['new_this_month']}"
        page.update()

    total_text = ft.Text("", size=theme.FONT_SM, color=theme.GRAY)

    def on_search(e):
        search_query["value"] = e.control.value
        refresh_table()

    # ── Layout ───────────────────────────────────────────────────────────────
    header_row = ft.Row(
        controls=[
            ft.Text("Hội viên", size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.SEARCH, color=theme.GRAY, size=16),
                                ft.TextField(
                                    hint_text="Tìm theo tên, SĐT, email...",
                                    border=ft.InputBorder.NONE,
                                    height=36,
                                    text_size=theme.FONT_SM,
                                    content_padding=ft.padding.symmetric(horizontal=4, vertical=0),
                                    expand=True,
                                    on_change=on_search,
                                ),
                            ],
                            spacing=theme.PAD_SM,
                        ),
                        bgcolor=theme.WHITE,
                        border_radius=theme.BUTTON_RADIUS,
                        border=ft.border.all(1, theme.BORDER),
                        padding=ft.padding.symmetric(horizontal=theme.PAD_MD, vertical=0),
                        width=280, height=40,
                    ),
                    ft.ElevatedButton(
                        "+ Thêm hội viên",
                        bgcolor=theme.ORANGE, color=theme.WHITE,
                        on_click=open_add_dialog,
                    ),
                ],
                spacing=theme.PAD_MD,
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    col_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Hội viên", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, expand=True),
                ft.Text("Email", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=180),
                ft.Text("Giới tính", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=80),
                ft.Text("Hành động", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=120),
            ],
        ),
        bgcolor=theme.BG,
        padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_SM),
    )

    member_table = ft.Container(
        content=ft.Column(
            controls=[col_header, table_body],
            spacing=0,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )

    page.overlay.append(member_dialog)
    page.overlay.append(confirm_dlg)

    main_content = ft.Column(
        controls=[
            Header(page),
            ft.Container(
                content=ft.Column(
                    controls=[
                        header_row,
                        total_text,
                        member_table,
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
        controls=[Sidebar(page, active_route="members"), main_content],
        spacing=0,
        expand=True,
    )
