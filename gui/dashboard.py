import flet as ft
from gui import theme
from gui.components.sidebar import Sidebar
from gui.components.header import Header


def stat_card(icon, label: str, value: str, badge_text: str, badge_color: str, badge_text_color: str = theme.WHITE) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(icon, color=theme.ORANGE, size=20),
                            width=40,
                            height=40,
                            bgcolor=theme.ORANGE_LIGHT,
                            border_radius=10,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(
                            content=ft.Text(badge_text, size=theme.FONT_XS, color=badge_text_color, weight=ft.FontWeight.W_600),
                            bgcolor=badge_color,
                            border_radius=theme.BADGE_RADIUS,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Text(value, size=theme.FONT_3XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                ft.Text(label, size=theme.FONT_SM, color=theme.GRAY),
            ],
            spacing=theme.PAD_SM,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=theme.PAD_XL,
        expand=True,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )


def member_row(name: str, initials: str, avatar_color: str, status: str, joined: str) -> ft.Container:
    if status == "Active":
        badge_color = theme.GREEN_LIGHT
        badge_text_color = theme.GREEN
    elif status == "Expired":
        badge_color = theme.AMBER_LIGHT
        badge_text_color = theme.AMBER
    else:
        badge_color = theme.BLUE_LIGHT
        badge_text_color = theme.BLUE

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(initials, color=theme.WHITE, size=theme.FONT_SM, weight=ft.FontWeight.BOLD),
                            width=36,
                            height=36,
                            bgcolor=avatar_color,
                            border_radius=18,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text(name, size=theme.FONT_SM, weight=ft.FontWeight.W_500, color=theme.TEXT_PRIMARY),
                    ],
                    spacing=theme.PAD_MD,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text(status, size=theme.FONT_XS, color=badge_text_color, weight=ft.FontWeight.W_600),
                    bgcolor=badge_color,
                    border_radius=theme.BADGE_RADIUS,
                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                    width=80,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Text(joined, size=theme.FONT_SM, color=theme.GRAY, width=100),
                ft.Container(
                    content=ft.Text("View", size=theme.FONT_XS, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                    border=ft.border.all(1, theme.ORANGE),
                    border_radius=6,
                    padding=ft.padding.symmetric(horizontal=12, vertical=4),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_MD),
        border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
    )


def revenue_chart(monthly_data: list[tuple[str, float]]) -> ft.Container:
    max_h = 120
    max_val = max((v for _, v in monthly_data), default=0)

    bars = []
    for i, (label, val) in enumerate(monthly_data):
        bar_h = int((val / max_val) * max_h) if max_val > 0 else 0
        bars.append(
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Container(
                            bgcolor=theme.ORANGE if i == len(monthly_data) - 1 else "#FED7AA",
                            border_radius=ft.border_radius.only(top_left=4, top_right=4),
                            height=bar_h,
                            width=28,
                        ),
                        height=max_h,
                        alignment=ft.Alignment.BOTTOM_CENTER,
                    ),
                    ft.Text(label, size=theme.FONT_XS, color=theme.GRAY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            )
        )

    total = sum(v for _, v in monthly_data)
    total_text = f"{int(total):,}đ"

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Revenue Overview", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text("Last 6 months", size=theme.FONT_XS, color=theme.GRAY),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=theme.PAD_MD),
                ft.Row(
                    controls=bars,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Container(height=theme.PAD_SM),
                ft.Row(
                    controls=[
                        ft.Text("Total: ", size=theme.FONT_SM, color=theme.GRAY),
                        ft.Text(total_text, size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.ORANGE),
                    ],
                ),
            ],
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=theme.PAD_XL,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )


def active_growth_chart(plan_stats: list[tuple[str, int]]) -> ft.Container:
    colors = [theme.ORANGE, theme.BLUE, theme.GREEN]
    max_count = max((c for _, c in plan_stats), default=0)

    rows = []
    for i, (plan_name, count) in enumerate(plan_stats):
        color = colors[i % len(colors)]
        pct = count / max_count if max_count > 0 else 0.0
        rows.append(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(plan_name, size=theme.FONT_SM, color=theme.TEXT_PRIMARY, expand=True),
                            ft.Text(str(count), size=theme.FONT_SM, weight=ft.FontWeight.W_600, color=color),
                        ],
                    ),
                    ft.ProgressBar(value=pct, color=color, bgcolor=theme.GRAY_LIGHT, height=6, border_radius=3),
                ],
                spacing=4,
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Active Growth", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                ft.Text("By membership type", size=theme.FONT_XS, color=theme.GRAY),
                ft.Container(height=theme.PAD_MD),
                *rows,
            ],
            spacing=theme.PAD_MD,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=theme.PAD_XL,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )


def package_card(name: str, price: str, period: str, member_count: int, duration_label: str, is_popular: bool = False) -> ft.Container:
    header_controls = [
        ft.Text(name, size=theme.FONT_MD, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
    ]
    if is_popular:
        header_controls.append(
            ft.Container(
                content=ft.Text("POPULAR", size=8, color=theme.WHITE, weight=ft.FontWeight.BOLD),
                bgcolor=theme.ORANGE,
                border_radius=4,
                padding=ft.padding.symmetric(horizontal=6, vertical=3),
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=header_controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row(
                    controls=[
                        ft.Text(price, size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.ORANGE),
                        ft.Text(f"/{period}", size=theme.FONT_SM, color=theme.GRAY),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.END,
                    spacing=4,
                ),
                ft.Divider(color=theme.BORDER, height=1),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.PEOPLE_ALT, color=theme.GRAY, size=14),
                        ft.Text(f"{member_count} members", size=theme.FONT_SM, color=theme.GRAY),
                    ],
                    spacing=4,
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ACCESS_TIME, color=theme.GRAY, size=14),
                        ft.Text(duration_label, size=theme.FONT_SM, color=theme.GRAY),
                    ],
                    spacing=4,
                ),
                ft.Container(
                    content=ft.Text("Manage", size=theme.FONT_SM, color=theme.ORANGE, weight=ft.FontWeight.W_600, text_align=ft.TextAlign.CENTER),
                    border=ft.border.all(1, theme.ORANGE),
                    border_radius=theme.BUTTON_RADIUS,
                    padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=8),
                    alignment=ft.Alignment.CENTER,
                    expand=True,
                ),
            ],
            spacing=theme.PAD_SM,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=theme.PAD_XL,
        border=ft.border.all(2, theme.ORANGE) if is_popular else ft.border.all(1, theme.BORDER),
        expand=True,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )


def equipment_card(name: str, wear_pct: float, purchased: str, status: str) -> ft.Container:
    if status == "Good":
        status_color = theme.GREEN
        status_bg = theme.GREEN_LIGHT
        bar_color = theme.GREEN
    elif status == "Fair":
        status_color = theme.AMBER
        status_bg = theme.AMBER_LIGHT
        bar_color = theme.AMBER
    else:
        status_color = theme.RED
        status_bg = theme.RED_LIGHT
        bar_color = theme.RED

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(name, size=theme.FONT_MD, weight=ft.FontWeight.W_600, color=theme.TEXT_PRIMARY, expand=True),
                        ft.Container(
                            content=ft.Text(status, size=theme.FONT_XS, color=status_color, weight=ft.FontWeight.W_600),
                            bgcolor=status_bg,
                            border_radius=theme.BADGE_RADIUS,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        ),
                    ],
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text("Wear Level", size=theme.FONT_XS, color=theme.GRAY, expand=True),
                                ft.Text(f"{int(wear_pct * 100)}%", size=theme.FONT_XS, color=bar_color, weight=ft.FontWeight.W_600),
                            ],
                        ),
                        ft.ProgressBar(value=wear_pct, color=bar_color, bgcolor=theme.GRAY_LIGHT, height=6, border_radius=3),
                    ],
                    spacing=4,
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.CALENDAR_TODAY_OUTLINED, color=theme.GRAY, size=12),
                        ft.Text(f"Purchased: {purchased}", size=theme.FONT_XS, color=theme.GRAY),
                    ],
                    spacing=4,
                ),
            ],
            spacing=theme.PAD_SM,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=theme.PAD_LG,
        expand=True,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )


def DashboardScreen(page: ft.Page) -> ft.Row:
    from app.services import member_svc, membership_svc, equipment_svc
    from app.repositories import member_repo, membership_repo, equipment_repo

    member_stats = member_svc.get_member_stats()
    revenue_stats = membership_svc.get_revenue_stats()
    eq_summary = equipment_svc.get_equipment_summary()
    expiring_subs = membership_repo.get_expiring_soon(days=7)
    expiring_count = len(expiring_subs)
    monthly_revenue = membership_svc.get_monthly_revenue(months=6)
    plan_stats = membership_svc.get_plan_subscription_stats()

    # --- KPI Stats ---
    stat_cards = ft.Row(
        controls=[
            stat_card(ft.Icons.PEOPLE_ALT, "Tổng hội viên", str(member_stats["active"]),
                      f"+{member_stats['new_this_month']} tháng này", theme.GREEN_LIGHT, theme.GREEN),
            stat_card(ft.Icons.SCHEDULE, "Sắp hết hạn", str(expiring_count),
                      "7 ngày tới", theme.AMBER_LIGHT, theme.AMBER),
            stat_card(ft.Icons.ATTACH_MONEY, "Doanh thu tháng", f"{int(revenue_stats['monthly']):,}đ",
                      f"Năm: {int(revenue_stats['yearly']):,}đ", theme.GREEN_LIGHT, theme.GREEN),
            stat_card(ft.Icons.BUILD, "Cần bảo trì", str(eq_summary["broken"] + eq_summary["maintenance"]),
                      "Thiết bị", theme.RED_LIGHT, theme.RED),
        ],
        spacing=theme.PAD_LG,
    )

    # --- Member Activity Table ---
    recent_members = member_repo.get_all()[:5]
    subs_map = {}
    for m in recent_members:
        active_subs = membership_repo.get_active_subscriptions_by_member(m.id)
        subs_map[m.id] = "Active" if active_subs else "Expired"

    colors_list = ["#8B5CF6", "#3B82F6", "#EC4899", "#10B981", "#F59E0B"]
    members_data = [
        (m.name,
         "".join(w[0].upper() for w in m.name.split()[:2]),
         colors_list[i % len(colors_list)],
         subs_map.get(m.id, "Expired"),
         m.created_at.strftime("%b %d, %Y"))
        for i, m in enumerate(recent_members)
    ]

    member_rows = [member_row(n, ini, c, s, j) for n, ini, c, s, j in members_data]

    member_table = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Recent Member Activity", size=theme.FONT_LG, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                            ft.Text("View All", size=theme.FONT_SM, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    padding=ft.padding.all(theme.PAD_LG),
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text("Member", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, expand=True),
                            ft.Text("Status", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=80),
                            ft.Text("Joined", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=100),
                            ft.Text("Action", size=theme.FONT_XS, color=theme.GRAY, weight=ft.FontWeight.W_600, width=60),
                        ],
                    ),
                    bgcolor=theme.BG,
                    padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_SM),
                ),
                ft.Column(controls=member_rows, spacing=0),
            ],
            spacing=0,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
        expand=True,
    )

    # --- Packages Section ---
    plans = membership_repo.get_all_plans(active_only=True)
    all_subs = membership_repo.get_all_subscriptions()
    from app.models.membership import MembershipSubscription
    active_subs_list = [s for s in all_subs if s.status == MembershipSubscription.STATUS_ACTIVE]
    sub_counts: dict = {}
    for s in active_subs_list:
        sub_counts[s.plan_id] = sub_counts.get(s.plan_id, 0) + 1
    popular_id = max(sub_counts, key=lambda pid: sub_counts[pid]) if sub_counts else None

    def _period_label(days: int) -> str:
        if days == 30:
            return "tháng"
        if days == 365:
            return "năm"
        return f"{days}ngày"

    if plans:
        pkg_controls = [
            package_card(
                name=p.name,
                price=f"{int(p.price):,}đ",
                period=_period_label(p.duration_days),
                member_count=sub_counts.get(p.id, 0),
                duration_label=f"{p.duration_days} ngày",
                is_popular=(p.id == popular_id),
            )
            for p in plans
        ]
    else:
        pkg_controls = [ft.Text("Chưa có gói tập nào", size=theme.FONT_SM, color=theme.GRAY)]

    packages_row = ft.Row(
        controls=pkg_controls,
        spacing=theme.PAD_LG,
    )

    packages_section = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Gym Packages", size=theme.FONT_XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                    ft.Text("Manage All", size=theme.FONT_SM, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            packages_row,
        ],
        spacing=theme.PAD_MD,
    )

    # --- Equipment Section ---
    from app.models.equipment import Equipment
    equipments = equipment_repo.get_all(active_only=True)[:4]

    def _eq_status(status: str) -> tuple[str, float]:
        if status == Equipment.STATUS_WORKING:
            return "Good", 0.25
        if status == Equipment.STATUS_MAINTENANCE:
            return "Fair", 0.65
        return "Poor", 0.90

    if equipments:
        eq_controls = [
            equipment_card(
                name=eq.name,
                wear_pct=_eq_status(eq.status)[1],
                purchased=str(eq.purchase_date) if eq.purchase_date else "N/A",
                status=_eq_status(eq.status)[0],
            )
            for eq in equipments
        ]
    else:
        eq_controls = [ft.Text("Chưa có thiết bị nào", size=theme.FONT_SM, color=theme.GRAY)]

    equipment_row = ft.Row(
        controls=eq_controls,
        spacing=theme.PAD_LG,
    )

    equipment_section = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Equipment Status", size=theme.FONT_XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                    ft.Text("View All", size=theme.FONT_SM, color=theme.ORANGE, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            equipment_row,
        ],
        spacing=theme.PAD_MD,
    )

    # --- [2.2] Expiring Soon Section ---
    all_members_map = {m.id: m.name for m in member_repo.get_all(active_only=False)}
    all_plans_map = {p.id: p.name for p in membership_repo.get_all_plans(active_only=False)}

    if expiring_subs:
        expiring_rows = []
        for s in expiring_subs:
            remaining = s.days_remaining()
            badge_color = theme.RED_LIGHT if remaining <= 3 else theme.AMBER_LIGHT
            badge_fg = theme.RED if remaining <= 3 else theme.AMBER
            expiring_rows.append(ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(all_members_map.get(s.member_id, "?"), size=theme.FONT_SM,
                                weight=ft.FontWeight.W_500, color=theme.TEXT_PRIMARY, expand=True),
                        ft.Text(all_plans_map.get(s.plan_id, "?"), size=theme.FONT_SM,
                                color=theme.GRAY, width=160),
                        ft.Text(s.end_date.strftime("%d/%m/%Y"), size=theme.FONT_SM,
                                color=theme.GRAY, width=90),
                        ft.Container(
                            content=ft.Text(f"Còn {remaining} ngày", size=theme.FONT_XS,
                                            color=badge_fg, weight=ft.FontWeight.W_600),
                            bgcolor=badge_color, border_radius=theme.BADGE_RADIUS,
                            padding=ft.padding.symmetric(horizontal=8, vertical=3),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(horizontal=theme.PAD_LG, vertical=theme.PAD_MD),
                border=ft.border.only(bottom=ft.BorderSide(1, theme.BORDER)),
            ))
        expiring_body = ft.Column(controls=expiring_rows, spacing=0)
    else:
        expiring_body = ft.Container(
            content=ft.Text("Không có gói tập nào sắp hết hạn trong 7 ngày tới.",
                            size=theme.FONT_SM, color=theme.GRAY),
            padding=ft.padding.all(theme.PAD_LG),
        )

    expiring_section = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=theme.AMBER, size=18),
                                ft.Text("Gói tập sắp hết hạn (7 ngày tới)",
                                        size=theme.FONT_LG, weight=ft.FontWeight.BOLD,
                                        color=theme.TEXT_PRIMARY),
                            ],
                            spacing=theme.PAD_SM,
                        ),
                        ft.Text("Xem tất cả", size=theme.FONT_SM, color=theme.ORANGE,
                                weight=ft.FontWeight.W_600),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                expiring_body,
            ],
            spacing=0,
        ),
        bgcolor=theme.CARD_BG,
        border_radius=theme.CARD_RADIUS,
        padding=ft.padding.only(left=0, right=0, top=theme.PAD_LG, bottom=0),
        shadow=ft.BoxShadow(blur_radius=4, color="#0000000A", offset=ft.Offset(0, 1)),
    )

    # --- Middle Row: member table + charts ---
    middle_row = ft.Row(
        controls=[
            member_table,
            ft.Column(
                controls=[
                    revenue_chart(monthly_revenue),
                    active_growth_chart(plan_stats),
                ],
                spacing=theme.PAD_LG,
                width=300,
            ),
        ],
        spacing=theme.PAD_LG,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # --- Footer ---
    footer = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text("GymAdmin Management System", size=theme.FONT_XS, color=theme.GRAY),
                ft.Text("v1.0.0  •  2026", size=theme.FONT_XS, color=theme.GRAY),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=ft.padding.symmetric(horizontal=theme.PAD_2XL, vertical=theme.PAD_LG),
        border=ft.border.only(top=ft.BorderSide(1, theme.BORDER)),
    )

    # --- Main Content ---
    main_content = ft.Column(
        controls=[
            Header(page),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Dashboard", size=theme.FONT_2XL, weight=ft.FontWeight.BOLD, color=theme.TEXT_PRIMARY),
                        ft.Text("Welcome back, Admin. Here's what's happening today.", size=theme.FONT_SM, color=theme.GRAY),
                        ft.Container(height=4),
                        stat_cards,
                        ft.Container(height=4),
                        expiring_section,
                        ft.Container(height=4),
                        middle_row,
                        ft.Container(height=4),
                        packages_section,
                        ft.Container(height=4),
                        equipment_section,
                        ft.Container(height=theme.PAD_LG),
                    ],
                    spacing=theme.PAD_LG,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                padding=ft.padding.all(theme.PAD_2XL),
                expand=True,
            ),
            footer,
        ],
        spacing=0,
        expand=True,
    )

    return ft.Row(
        controls=[
            Sidebar(page, active_route="dashboard"),
            main_content,
        ],
        spacing=0,
        expand=True,
    )
