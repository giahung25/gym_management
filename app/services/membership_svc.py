from datetime import datetime
from app.models.membership import MembershipPlan, MembershipSubscription
from app.repositories import membership_repo


def create_plan(name: str, duration_days: int, price: float,
                description: str = None) -> MembershipPlan:
    if not name or not name.strip():
        raise ValueError("Tên gói tập không được để trống")
    if duration_days <= 0:
        raise ValueError("Số ngày phải lớn hơn 0")
    if price < 0:
        raise ValueError("Giá không được âm")
    plan = MembershipPlan(
        name=name.strip(),
        duration_days=duration_days,
        price=price,
        description=description,
    )
    return membership_repo.create_plan(plan)


def update_plan(plan: MembershipPlan, name: str = None, duration_days: int = None,
                price: float = None, description: str = None) -> MembershipPlan:
    if name is not None:
        plan.name = name.strip()
    if duration_days is not None:
        plan.duration_days = duration_days
    if price is not None:
        plan.price = price
    if description is not None:
        plan.description = description
    return membership_repo.update_plan(plan)


def subscribe_member(member_id: str, plan_id: str,
                     price_paid: float = None, start_date: datetime = None) -> MembershipSubscription:
    plan = membership_repo.get_plan_by_id(plan_id)
    if not plan:
        raise ValueError("Không tìm thấy gói tập")
    sub = MembershipSubscription(
        member_id=member_id,
        plan_id=plan_id,
        duration_days=plan.duration_days,
        price_paid=price_paid if price_paid is not None else plan.price,
        start_date=start_date or datetime.now(),
    )
    return membership_repo.create_subscription(sub)


def cancel_subscription(sub_id: str) -> MembershipSubscription:
    sub = membership_repo.get_subscription_by_id(sub_id)
    if not sub:
        raise ValueError("Không tìm thấy đăng ký gói tập")
    if sub.status != MembershipSubscription.STATUS_ACTIVE:
        raise ValueError("Chỉ có thể hủy gói tập đang active")
    sub.cancel()
    return membership_repo.update_subscription(sub)


def auto_expire_subscriptions():
    membership_repo.expire_old_subscriptions()


def get_monthly_revenue(months: int = 6) -> list[tuple[str, float]]:
    subs = membership_repo.get_all_subscriptions()
    now = datetime.now()
    result = []
    for i in range(months - 1, -1, -1):
        month = now.month - i
        year = now.year
        while month <= 0:
            month += 12
            year -= 1
        total = sum(
            s.price_paid for s in subs
            if s.created_at.year == year and s.created_at.month == month
        )
        result.append((f"T{month}", total))
    return result


def get_plan_subscription_stats() -> list[tuple[str, int]]:
    plans = membership_repo.get_all_plans(active_only=True)
    subs = membership_repo.get_all_subscriptions()
    active_subs = [s for s in subs if s.status == MembershipSubscription.STATUS_ACTIVE]
    sub_counts: dict[str, int] = {}
    for s in active_subs:
        sub_counts[s.plan_id] = sub_counts.get(s.plan_id, 0) + 1
    stats = [(p.name, sub_counts.get(p.id, 0)) for p in plans]
    stats.sort(key=lambda x: x[1], reverse=True)
    return stats[:3]


def get_revenue_stats() -> dict:
    subs = membership_repo.get_all_subscriptions()
    now = datetime.now()
    monthly = sum(
        s.price_paid for s in subs
        if s.created_at.year == now.year and s.created_at.month == now.month
    )
    yearly = sum(s.price_paid for s in subs if s.created_at.year == now.year)
    total = sum(s.price_paid for s in subs)
    return {
        "monthly": monthly,
        "yearly": yearly,
        "total": total,
    }
