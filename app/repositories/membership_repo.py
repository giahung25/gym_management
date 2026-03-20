from app.core.database import get_db
from app.models.membership import MembershipPlan, MembershipSubscription
from datetime import datetime, timedelta


def _row_to_plan(row) -> MembershipPlan:
    p = MembershipPlan.__new__(MembershipPlan)
    p.id = row["id"]
    p.name = row["name"]
    p.duration_days = row["duration_days"]
    p.price = row["price"]
    p.description = row["description"]
    p.created_at = datetime.fromisoformat(row["created_at"])
    p.updated_at = datetime.fromisoformat(row["updated_at"])
    p.is_active = bool(row["is_active"])
    return p


def _row_to_sub(row) -> MembershipSubscription:
    s = MembershipSubscription.__new__(MembershipSubscription)
    s.id = row["id"]
    s.member_id = row["member_id"]
    s.plan_id = row["plan_id"]
    s.price_paid = row["price_paid"]
    s.start_date = datetime.fromisoformat(row["start_date"])
    s.end_date = datetime.fromisoformat(row["end_date"])
    s.status = row["status"]
    s.created_at = datetime.fromisoformat(row["created_at"])
    s.updated_at = datetime.fromisoformat(row["updated_at"])
    s.is_active = bool(row["is_active"])
    return s


# --- MembershipPlan CRUD ---

def create_plan(plan: MembershipPlan) -> MembershipPlan:
    with get_db() as conn:
        conn.execute(
            """INSERT INTO membership_plans (id, name, duration_days, price, description,
               created_at, updated_at, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (plan.id, plan.name, plan.duration_days, plan.price, plan.description,
             plan.created_at.isoformat(), plan.updated_at.isoformat(), int(plan.is_active))
        )
    return plan


def get_plan_by_id(id: str) -> MembershipPlan | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM membership_plans WHERE id = ?", (id,)).fetchone()
    return _row_to_plan(row) if row else None


def get_all_plans(active_only: bool = True) -> list[MembershipPlan]:
    with get_db() as conn:
        if active_only:
            rows = conn.execute("SELECT * FROM membership_plans WHERE is_active = 1 ORDER BY price").fetchall()
        else:
            rows = conn.execute("SELECT * FROM membership_plans ORDER BY price").fetchall()
    return [_row_to_plan(r) for r in rows]


def update_plan(plan: MembershipPlan) -> MembershipPlan:
    plan.update()
    with get_db() as conn:
        conn.execute(
            """UPDATE membership_plans SET name=?, duration_days=?, price=?, description=?,
               updated_at=?, is_active=? WHERE id=?""",
            (plan.name, plan.duration_days, plan.price, plan.description,
             plan.updated_at.isoformat(), int(plan.is_active), plan.id)
        )
    return plan


def delete_plan(id: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE membership_plans SET is_active = 0, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), id)
        )


# --- MembershipSubscription CRUD ---

def create_subscription(sub: MembershipSubscription) -> MembershipSubscription:
    with get_db() as conn:
        conn.execute(
            """INSERT INTO subscriptions (id, member_id, plan_id, price_paid,
               start_date, end_date, status, created_at, updated_at, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (sub.id, sub.member_id, sub.plan_id, sub.price_paid,
             sub.start_date.isoformat(), sub.end_date.isoformat(), sub.status,
             sub.created_at.isoformat(), sub.updated_at.isoformat(), int(sub.is_active))
        )
    return sub


def get_subscription_by_id(id: str) -> MembershipSubscription | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM subscriptions WHERE id = ?", (id,)).fetchone()
    return _row_to_sub(row) if row else None


def get_all_subscriptions() -> list[MembershipSubscription]:
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM subscriptions ORDER BY start_date DESC").fetchall()
    return [_row_to_sub(r) for r in rows]


def get_subscriptions_by_member(member_id: str) -> list[MembershipSubscription]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM subscriptions WHERE member_id = ? ORDER BY start_date DESC", (member_id,)
        ).fetchall()
    return [_row_to_sub(r) for r in rows]


def get_active_subscriptions_by_member(member_id: str) -> list[MembershipSubscription]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM subscriptions WHERE member_id = ? AND status = 'active' ORDER BY end_date",
            (member_id,)
        ).fetchall()
    return [_row_to_sub(r) for r in rows]


def get_expiring_soon(days: int = 7) -> list[MembershipSubscription]:
    cutoff = (datetime.now() + timedelta(days=days)).isoformat()
    now = datetime.now().isoformat()
    with get_db() as conn:
        rows = conn.execute(
            """SELECT * FROM subscriptions WHERE status = 'active'
               AND end_date <= ? AND end_date >= ? ORDER BY end_date""",
            (cutoff, now)
        ).fetchall()
    return [_row_to_sub(r) for r in rows]


def update_subscription(sub: MembershipSubscription) -> MembershipSubscription:
    sub.update()
    with get_db() as conn:
        conn.execute(
            """UPDATE subscriptions SET status=?, price_paid=?, start_date=?, end_date=?,
               updated_at=?, is_active=? WHERE id=?""",
            (sub.status, sub.price_paid, sub.start_date.isoformat(), sub.end_date.isoformat(),
             sub.updated_at.isoformat(), int(sub.is_active), sub.id)
        )
    return sub


def expire_old_subscriptions():
    now = datetime.now().isoformat()
    with get_db() as conn:
        conn.execute(
            "UPDATE subscriptions SET status='expired', updated_at=? WHERE status='active' AND end_date < ?",
            (now, now)
        )
