import flet as ft
from gui import theme
from gui.components.header import Header
from gui.components.sidebar import Sidebar
from app.repositories import membership_repo, member_repo
from app.services import membership_svc


def MembershipsScreen(page: ft.Page) -> ft.Row:
    # ── Plan Tab ─────────────────────────────────────────────────────────────
    plans_body = ft.Column(controls=[], spacing=0)
    selected_plan = {"obj": None}

    fp_name = ft.TextField(label="Tên gói *", expand=True)
    fp_days = ft.TextField(label="Số ngày *", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    fp_price = ft.TextField(label="Giá (VND) *", expand=True, keyboard_type=ft.KeyboardType.NUMBER)
    fp_desc = ft.TextField(label="Mô tả", expand=True, multiline=True, min_lines=2)
    plan_dialog_error = ft.Text("", color=theme.RED, size=theme.FONT_SM)
    plan_dialog_title = ft.Text("", size=theme.FONT_LG, weight=ft.FontWeight.BOLD)

    def save_plan(e):
        try:
            days = int(fp_days.value or 0)
            price = float(fp_price.value or 0)
            if selected_plan["obj"] is None:
                membership_svc.create_plan(
                    name=fp_name.value,
                    duration_days=days,
                    price=price,
                    description=fp_desc.value or None,
                )
            else:
                p = selected_plan["obj"]
                membership_svc.update_plan(p, name=fp_name.value, duration_days=days,
                                           price=price, description=fp_desc.value or None)
            plan_dialog.open = False
            page.update()
            refresh_plans()
        except (ValueError, TypeError) as ex:
            plan_dialog_error.value = str(ex)
            page.update()

    plan_dialog = ft.AlertDialog(
        modal=True,
        title=plan_dialog_title,
        content=ft.Column(
            controls=[
                ft.Row(controls=[fp_name], spacing=theme.PAD_MD),
                ft.Row(controls=[fp_days, fp_price], spacing=theme.PAD_MD),
                fp_desc,
                plan_dialog_error,
            ],
            spacing=theme.PAD_MD, width=480, tight=True,
        ),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: setattr(plan_dialog, "open", False) or page.update()),
            ft.ElevatedButton("Lưu", on_click=save_plan, bgcolor=theme.ORANGE, color=theme.WHITE),
        ],
    )

    def open_add_plan(e):
        selected_plan["obj"] = None
        fp_name.value = fp_days.value = fp_price.value = fp_desc.value = ""
        plan_dialog_error.value = ""
        plan_dialog_title.value = "Thêm gói tập mới"
        plan_dialog.open = True
        page.update()

    def open_edit_plan(p):
        selected_plan["obj"] = p
        fp_name.value = p.name
        fp_days.value = str(p.duration_days)
        fp_price.value = str(int(p.price))
        fp_desc.value = p.description or ""
        plan_dialog_error.value = ""
        plan_dialog_title.value = "Chỉnh sửa gói tập"
        plan_dialog.open = True
        page.update()

    delete_plan_id = {"id": None}
    confirm_plan_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Xác nhận xóa gói tập"),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: setattr(confirm_plan_dlg, "open", False) or page.update()),
            ft.ElevatedButton("Xóa", bgcolor=theme.RED, color=theme.WHITE,
                              on_click=lambda e: [membership_repo.delete_plan(delete_plan_id["id"]),
                                                  setattr(confirm_plan_dlg, "open", False),
                                                  page.update(), refresh_plans()]),
        ],
    )

    def refresh_plans():
        plans = membership_repo.get_all_plans()
        rows = []
        for p in plans:
            rows.append(ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(p.name, size=theme.FONT_MD, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY),
                                ft.Text(f"{p.duration_days} ngày  •  {p.description or ''}", size=theme.FONT_XS, color=theme.GRAY),
                            ],
                            spacing=2, expand=True,
                        ),
                        ft.Text(f"{int(p.price):,}đ", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.ORANGE, width=120),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text("Sửa", size=theme.FONT_XS, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                                    border=ft.border.all(1, theme.ORANGE), border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    on_click=lambda e, plan=p: open_edit_plan(plan),
                                ),
                                ft.Container(
                                    content=ft.Text("Xóa", size=theme.FONT_XS, color=theme.RED, weight=ft.FontWeight.W_600),
                                    border=ft.border.all(1, theme.RED), border_radius=6,
                                    padding=ft.padding.symmetric(horizontal=10, vertical=3),
                                    on_click=lambda e, plan=p: [
                                        delete_plan_id.update({"id": plan.id}),
                                        setattr(confirm_plan_dlg, "open", True),
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
        plans_body.controls = rows
        page.update()

    # ── Subscription Tab ─────────────────────────────────────────────────────
    subs_body = ft.Column(controls=[], spacing=0)

    fs_member = ft.Dropdown(label="Hội viên *", expand=True)
    fs_plan = ft.Dropdown(label="Gói tập *", expand=True)
    fs_price = ft.TextField(label="Giá thực tế (để trống = giá gói)", expand=True,
                            keyboard_type=ft.KeyboardType.NUMBER)
    fs_start = ft.TextField(label="Ngày bắt đầu (YYYY-MM-DD, để trống = hôm nay)", expand=True)
    sub_dialog_error = ft.Text("", color=theme.RED, size=theme.FONT_SM)

    def save_sub(e):
        try:
            from datetime import datetime as dt
            start = dt.fromisoformat(fs_start.value) if fs_start.value.strip() else None
            price = float(fs_price.value) if fs_price.value.strip() else None
            membership_svc.subscribe_member(
                member_id=fs_member.value,
                plan_id=fs_plan.value,
                price_paid=price,
                start_date=start,
            )
            sub_dialog.open = False
            page.update()
            refresh_subs()
        except Exception as ex:
            sub_dialog_error.value = str(ex)
            page.update()

    sub_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Đăng ký gói tập", size=theme.FONT_LG, weight=ft.FontWeight.BOLD),
        content=ft.Column(
            controls=[
                ft.Row(controls=[fs_member, fs_plan], spacing=theme.PAD_MD),
                ft.Row(controls=[fs_price, fs_start], spacing=theme.PAD_MD),
                sub_dialog_error,
            ],
            spacing=theme.PAD_MD, width=540, tight=True,
        ),
        actions=[
            ft.TextButton("Hủy", on_click=lambda e: setattr(sub_dialog, "open", False) or page.update()),
            ft.ElevatedButton("Đăng ký", on_click=save_sub, bgcolor=theme.ORANGE, color=theme.WHITE),
        ],
    )

    def open_add_sub(e):
        members = member_repo.get_all()
        plans = membership_repo.get_all_plans()
        fs_member.options = [ft.dropdown.Option(m.id, m.name) for m in members]
        fs_plan.options = [ft.dropdown.Option(p.id, f"{p.name} ({p.duration_days}d - {int(p.price):,}đ)") for p in plans]
        fs_member.value = fs_plan.value = None
        fs_price.value = fs_start.value = ""
        sub_dialog_error.value = ""
        sub_dialog.open = True
        page.update()

    STATUS_COLORS = {
        "active": (theme.GREEN_LIGHT, theme.GREEN),
        "expired": (theme.AMBER_LIGHT, theme.AMBER),
        "cancelled": (theme.RED_LIGHT, theme.RED),
    }

    def refresh_subs():
        membership_svc.auto_expire_subscriptions()
        subs = membership_repo.get_all_subscriptions()
        members_map = {m.id: m.name for m in member_repo.get_all(active_only=False)}
        plans_map = {p.id: p.name for p in membership_repo.get_all_plans(active_only=False)}
        rows = []
        for s in subs:
            bg, fg = STATUS_COLORS.get(s.status, (theme.GRAY_LIGHT, theme.GRAY))
            rows.append(ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(members_map.get(s.member_id, "?"), size=theme.FONT_SM,
                                weight=ft.FontWeight.W_500, color=theme.TEXT_PRIMARY, expand=True),
                        ft.Text(plans_map.get(s.plan_id, "?"), size=theme.FONT_SM, color=theme.GRAY, width=160),
                        ft.Text(s.start_date.strftime("%d/%m/%Y"), size=theme.FONT_SM, color=theme.GRAY, width=100),
                        ft.Text(s.end_date.strftime("%d/%m/%Y"), size=theme.FONT_SM, color=theme.GRAY, width=100),
                        ft.Container(
                            content=ft.Text(s.status, size=theme.FONT_XS, color=fg, weight=ft.FontWeight.W_600),
                            bgcolor=bg, border_radius=theme.BADGE_RADIUS,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3), width=80,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text(f"{int(s.price_paid):,}đ", size=theme.FONT_SM, color=theme.ORANGE, width=100),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_MD),
                border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
            ))
        subs_body.controls = rows
        page.update()

    # ── Tabs ─────────────────────────────────────────────────────────────────
    page.overlay.extend([plan_dialog, confirm_plan_dlg, sub_dialog])

    plans_tab_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Danh sách gói tập", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.ElevatedButton("+ Thêm gói", bgcolor=theme.ORANGE, color=theme.WHITE, on_click=open_add_plan),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Column(controls=[plans_body], spacing=0),
                    bgcolor=theme.CARD_BG,
                    border_radius=theme.CARD_RADIUS,
                    shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
                ),
            ],
            spacing=theme.PAD_LG,
        ),
        padding=ft.padding.all(theme.PAD_2XL),
    )

    subs_col_header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("Hội viên", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, expand=True),
                ft.Text("Gói tập", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=160),
                ft.Text("Bắt đầu", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=100),
                ft.Text("Kết thúc", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=100),
                ft.Text("Trạng thái", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=80),
                ft.Text("Giá trả", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=100),
            ],
        ),
        bgcolor=theme.BG,
        padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_SM),
    )

    subs_tab_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Đăng ký gói tập", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.ElevatedButton("+ Đăng ký mới", bgcolor=theme.ORANGE, color=theme.WHITE, on_click=open_add_sub),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Column(controls=[subs_col_header, subs_body], spacing=0),
                    bgcolor=theme.CARD_BG,
                    border_radius=theme.CARD_RADIUS,
                    shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
                ),
            ],
            spacing=theme.PAD_LG,
        ),
        padding=ft.padding.all(theme.PAD_2XL),
    )
    def on_tab_change(e):
        if e.control.selected_index == 0:
            refresh_plans()
        else:
            refresh_subs()

    tabs = ft.Tabs(
        selected_index=0,
        length=2,
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="Gói tập"),
                        ft.Tab(label="Đăng ký"),
                    ],
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        plans_tab_content,
                        subs_tab_content,
                    ],
            
                ),
            ],
        ),
        on_change=on_tab_change,
    )

    main_content = ft.Column(
        controls=[
            Header(page),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Gói tập & Đăng ký", size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        tabs,
                    ],
                    spacing=theme.PAD_LG,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.only(left=theme.PAD_2XL, right=theme.PAD_2XL, top=theme.PAD_2XL),
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )

    refresh_plans()

    return ft.Row(
        controls=[Sidebar(page, active_route="packages"), main_content],
        spacing=0,
        expand=True,
    )
