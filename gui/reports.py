import flet as ft
from gui import theme
from gui.components.header import Header
from gui.components.sidebar import Sidebar
from app.services import member_svc, membership_svc, equipment_svc
from app.repositories import membership_repo


def ReportsScreen(page: ft.Page) -> ft.Row:

    def build_content():
        member_stats = member_svc.get_member_stats()
        revenue_stats = membership_svc.get_revenue_stats()
        eq_summary = equipment_svc.get_equipment_summary()
        expiring = membership_repo.get_expiring_soon(days=7)

        from app.repositories import member_repo
        members_map = {m.id: m.name for m in member_repo.get_all(active_only=False)}
        from app.repositories import membership_repo as mr
        plans_map = {p.id: p.name for p in mr.get_all_plans(active_only=False)}

        def kpi_card(label, value, color=theme.TEXT_PRIMARY):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(value, size=theme.FONT_3XL, weight=ft.FontWeight.BOLD, color=color),
                        ft.Text(label, size=theme.FONT_SM, color=theme.GRAY),
                    ],
                    spacing=4,
                ),
                bgcolor=theme.CARD_BG,
                border_radius=theme.CARD_RADIUS,
                padding=theme.PAD_XL,
                expand=True,
                shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
            )

        kpi_row = ft.Row(
            controls=[
                kpi_card("Tổng hội viên", str(member_stats["total"])),
                kpi_card("Hội viên active", str(member_stats["active"]), theme.GREEN),
                kpi_card("Mới tháng này", str(member_stats["new_this_month"]), theme.BLUE),
                kpi_card("Doanh thu tháng này", f"{int(revenue_stats['monthly']):,}đ", theme.ORANGE),
                kpi_card("Doanh thu năm nay", f"{int(revenue_stats['yearly']):,}đ", theme.ORANGE),
            ],
            spacing=theme.PAD_LG,
        )

        eq_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Tình trạng thiết bị", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(str(eq_summary["working"]), size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.GREEN),
                                    ft.Text("Hoạt động", size=theme.FONT_SM, color=theme.GRAY),
                                ],
                                spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(str(eq_summary["maintenance"]), size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.AMBER),
                                    ft.Text("Bảo trì", size=theme.FONT_SM, color=theme.GRAY),
                                ],
                                spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(str(eq_summary["broken"]), size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.RED),
                                    ft.Text("Hỏng", size=theme.FONT_SM, color=theme.GRAY),
                                ],
                                spacing=2, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=theme.PAD_2XL,
                    ),
                ],
                spacing=theme.PAD_MD,
            ),
            bgcolor=theme.CARD_BG, border_radius=theme.CARD_RADIUS,
            padding=theme.PAD_XL,
            shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
        )

        expiring_rows = []
        for s in expiring:
            remaining = s.days_remaining()
            expiring_rows.append(ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(members_map.get(s.member_id, "?"), size=theme.FONT_SM,
                                weight=ft.FontWeight.W_500, color=theme.TEXT_PRIMARY, expand=True),
                        ft.Text(plans_map.get(s.plan_id, "?"), size=theme.FONT_SM, color=theme.GRAY, width=160),
                        ft.Text(s.end_date.strftime("%d/%m/%Y"), size=theme.FONT_SM, color=theme.GRAY, width=100),
                        ft.Container(
                            content=ft.Text(f"Còn {remaining} ngày", size=theme.FONT_XS,
                                            color=theme.RED if remaining <= 3 else theme.AMBER,
                                            weight=ft.FontWeight.W_600),
                            bgcolor=theme.RED_LIGHT if remaining <= 3 else theme.AMBER_LIGHT,
                            border_radius=theme.BADGE_RADIUS,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_MD),
                border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
            ))

        expiring_section = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Gói tập sắp hết hạn (7 ngày tới)", size=theme.FONT_LG,
                            weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                    ft.Container(
                        content=ft.Column(
                            controls=expiring_rows if expiring_rows else [
                                ft.Text("Không có gói tập nào sắp hết hạn.", size=theme.FONT_SM, color=theme.GRAY)
                            ],
                            spacing=0,
                        ),
                        bgcolor=theme.CARD_BG, border_radius=theme.CARD_RADIUS,
                        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
                    ),
                ],
                spacing=theme.PAD_MD,
            ),
        )

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Báo cáo", size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.ElevatedButton("Làm mới", bgcolor=theme.ORANGE, color=theme.WHITE,
                                          on_click=lambda e: refresh()),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                kpi_row,
                ft.Row(controls=[eq_section], spacing=theme.PAD_LG),
                expiring_section,
            ],
            spacing=theme.PAD_LG,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    content_area = ft.Container(expand=True)

    def refresh():
        content_area.content = build_content()
        page.update()

    content_area.content = build_content()

    main_content = ft.Column(
        controls=[
            Header(page),
            ft.Container(
                content=content_area,
                padding=ft.padding.all(theme.PAD_2XL),
                expand=True,
            ),
        ],
        spacing=0,
        expand=True,
    )

    return ft.Row(
        controls=[Sidebar(page, active_route="reports"), main_content],
        spacing=0,
        expand=True,
    )
