import flet as ft
from gui import theme
from gui.components.header import Header
from gui.components.sidebar import Sidebar
from app.repositories import member_repo, membership_repo
from app.services import member_svc


def MembersScreen(page: ft.Page) -> ft.Row:
    # State
    search_query = {"value": ""}
    selected_member = {"obj": None}
    filter_gender = {"value": None}       # None = tất cả
    filter_sub_status = {"value": None}   # None | "active" | "no_active"

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
            ft.TextButton("Hủy", on_click=lambda e: setattr(member_dialog, "open", False) or page.update()),
            ft.ElevatedButton("Lưu", on_click=save_member, bgcolor=theme.ORANGE, color=theme.WHITE),
        ],
    )

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

    # ── [2.1] Dialog: Chi tiết hội viên — lịch sử gói tập ──────────────────
    detail_body = ft.Column(controls=[], spacing=0, scroll=ft.ScrollMode.AUTO)
    detail_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Lịch sử gói tập", size=theme.FONT_LG, weight=ft.FontWeight.BOLD),
        content=ft.Container(content=detail_body, width=540, height=320),
        actions=[
            ft.TextButton("Đóng", on_click=lambda e: setattr(detail_dialog, "open", False) or page.update()),
        ],
    )

    STATUS_COLORS = {
        "active": (theme.GREEN_LIGHT, theme.GREEN),
        "expired": (theme.AMBER_LIGHT, theme.AMBER),
        "cancelled": (theme.RED_LIGHT, theme.RED),
    }

    def open_detail_dialog(m):
        subs = membership_repo.get_subscriptions_by_member(m.id)
        plans_map = {p.id: p.name for p in membership_repo.get_all_plans(active_only=False)}
        if not subs:
            detail_body.controls = [
                ft.Text("Chưa có lịch sử đăng ký gói tập.", size=theme.FONT_SM, color=theme.GRAY)
            ]
        else:
            rows = []
            for s in subs:
                bg, fg = STATUS_COLORS.get(s.status, (theme.GRAY_LIGHT, theme.GRAY))
                rows.append(ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(plans_map.get(s.plan_id, "?"), size=theme.FONT_SM,
                                            weight=ft.FontWeight.W_500, color=theme.TEXT_PRIMARY),
                                    ft.Text(
                                        f"{s.start_date.strftime('%d/%m/%Y')} → {s.end_date.strftime('%d/%m/%Y')}",
                                        size=theme.FONT_XS, color=theme.GRAY,
                                    ),
                                ],
                                spacing=2, expand=True,
                            ),
                            ft.Container(
                                content=ft.Text(s.status, size=theme.FONT_XS, color=fg, weight=ft.FontWeight.W_600),
                                bgcolor=bg, border_radius=theme.BADGE_RADIUS,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                            ),
                            ft.Text(f"{int(s.price_paid):,}đ", size=theme.FONT_SM,
                                    color=theme.ORANGE, width=90),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=theme.PAD_MD, vertical=theme.PAD_MD),
                    border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
                ))
            detail_body.controls = rows
        detail_dialog.title = ft.Text(
            f"Lịch sử gói tập — {m.name}",
            size=theme.FONT_LG, weight=ft.FontWeight.BOLD,
        )
        detail_dialog.open = True
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
                                content=ft.Text(initials, color=theme.WHITE, size=theme.FONT_SM,
                                                weight=ft.FontWeight.BOLD),
                                width=36, height=36, bgcolor=avatar_color,
                                border_radius=18, alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(m.name, size=theme.FONT_SM, weight=ft.FontWeight.W_500,
                                            color=theme.TEXT_PRIMARY),
                                    ft.Text(m.phone, size=theme.FONT_XS, color=theme.GRAY),
                                ],
                                spacing=0, tight=True,
                            ),
                        ],
                        spacing=theme.PAD_MD, expand=True,
                    ),
                    ft.Text(m.email or "—", size=theme.FONT_SM, color=theme.GRAY, width=180),
                    ft.Text(
                        {"male": "Nam", "female": "Nữ", "other": "Khác"}.get(m.gender or "", "—"),
                        size=theme.FONT_SM, color=theme.GRAY, width=60,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text("Chi tiết", size=theme.FONT_XS, color=theme.BLUE,
                                                weight=ft.FontWeight.W_600),
                                border=ft.border.all(1, theme.BLUE), border_radius=6,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                on_click=lambda e, member=m: open_detail_dialog(member),
                            ),
                            ft.Container(
                                content=ft.Text("Sửa", size=theme.FONT_XS, color=theme.ORANGE,
                                                weight=ft.FontWeight.W_600),
                                border=ft.border.all(1, theme.ORANGE), border_radius=6,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                on_click=lambda e, member=m: open_edit_dialog(member),
                            ),
                            ft.Container(
                                content=ft.Text("Xóa", size=theme.FONT_XS, color=theme.RED,
                                                weight=ft.FontWeight.W_600),
                                border=ft.border.all(1, theme.RED), border_radius=6,
                                padding=ft.padding.symmetric(horizontal=8, vertical=3),
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

    # ── [2.3] Refresh với filter ─────────────────────────────────────────────
    def refresh_table():
        kw = search_query["value"].strip()
        members = member_repo.search(kw) if kw else member_repo.get_all()

        # Filter giới tính
        gf = filter_gender["value"]
        if gf:
            members = [m for m in members if m.gender == gf]

        # Filter trạng thái subscription
        sf = filter_sub_status["value"]
        if sf:
            active_ids = {
                s.member_id
                for s in membership_repo.get_all_subscriptions()
                if s.status == "active"
            }
            if sf == "active":
                members = [m for m in members if m.id in active_ids]
            else:
                members = [m for m in members if m.id not in active_ids]

        table_body.controls = [_make_row(m) for m in members]
        stats = member_svc.get_member_stats()
        total_text.value = (
            f"Tổng: {stats['total']}  |  Active: {stats['active']}  |  Mới tháng này: {stats['new_this_month']}"
            + (f"  |  Đang lọc: {len(members)}" if gf or sf else "")
        )
        page.update()

    total_text = ft.Text("", size=theme.FONT_SM, color=theme.GRAY)

    def on_search(e):
        search_query["value"] = e.control.value
        refresh_table()

    # ── [2.3] Filter controls ─────────────────────────────────────────────────
    gender_filter = ft.Dropdown(
        label="Giới tính",
        width=130,
        border=ft.InputBorder.UNDERLINE,
        enable_filter=True,
        editable=True,
        leading_icon=ft.Icons.SEARCH,
        options=[
            ft.dropdown.Option("", "Tất cả"),
            ft.dropdown.Option("male", "Nam"),
            ft.dropdown.Option("female", "Nữ"),
            ft.dropdown.Option("other", "Khác"),
        ],
        value="",
    )

    def on_gender_change(e):
        filter_gender.update({"value": e.control.value or None})
        refresh_table()

    gender_filter.on_change = on_gender_change

    sub_status_filter = ft.Dropdown(
        label="Gói tập",
        width=150,
        border=ft.InputBorder.UNDERLINE,
        enable_filter=True,
        editable=True,
        leading_icon=ft.Icons.SEARCH,
        options=[
            ft.dropdown.Option("", "Tất cả"),
            ft.dropdown.Option("active", "Đang active"),
            ft.dropdown.Option("no_active", "Không active"),
        ],
        value="",
    )

    def on_sub_status_change(e):
        filter_sub_status.update({"value": e.control.value or None})
        refresh_table()

    sub_status_filter.on_change = on_sub_status_change

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
                        width=260, height=40,
                    ),
                    gender_filter,
                    sub_status_filter,
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
                ft.Text("Hội viên", size=theme.FONT_XS, color=theme.GRAY,
                        weight=ft.FontWeight.W_600, expand=True),
                ft.Text("Email", size=theme.FONT_XS, color=theme.GRAY,
                        weight=ft.FontWeight.W_600, width=180),
                ft.Text("Giới tính", size=theme.FONT_XS, color=theme.GRAY,
                        weight=ft.FontWeight.W_600, width=60),
                ft.Text("Hành động", size=theme.FONT_XS, color=theme.GRAY,
                        weight=ft.FontWeight.W_600, width=170),
            ],
        ),
        bgcolor=theme.BG,
        padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_SM),
    )

    member_table = ft.Container(
        content=ft.Column(controls=[col_header, table_body], spacing=0),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )

    page.overlay.extend([member_dialog, confirm_dlg, detail_dialog])

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

    # Đăng ký callback cho header search bar
    def _header_search(value: str):
        search_query["value"] = value
        refresh_table()

    page.on_search_change = _header_search

    refresh_table()

    return ft.Row(
        controls=[Sidebar(page, active_route="members"), main_content],
        spacing=0,
        expand=True,
    )
