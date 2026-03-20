from app.core.database import get_db
from app.models.member import Member
from datetime import datetime


def _row_to_member(row) -> Member:
    m = Member.__new__(Member)
    m.id = row["id"]
    m.name = row["name"]
    m.phone = row["phone"]
    m.email = row["email"]
    m.gender = row["gender"]
    m.date_of_birth = row["date_of_birth"]
    m.address = row["address"]
    m.emergency_contact = row["emergency_contact"]
    m.created_at = datetime.fromisoformat(row["created_at"])
    m.updated_at = datetime.fromisoformat(row["updated_at"])
    m.is_active = bool(row["is_active"])
    return m


def create(member: Member) -> Member:
    with get_db() as conn:
        conn.execute(
            """INSERT INTO members (id, name, phone, email, gender, date_of_birth,
               address, emergency_contact, photo, created_at, updated_at, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (member.id, member.name, member.phone, member.email, member.gender,
             member.date_of_birth, member.address, member.emergency_contact, None,
             member.created_at.isoformat(), member.updated_at.isoformat(), int(member.is_active))
        )
    return member


def get_by_id(id: str) -> Member | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM members WHERE id = ?", (id,)).fetchone()
    return _row_to_member(row) if row else None


def get_all(active_only: bool = True) -> list[Member]:
    with get_db() as conn:
        if active_only:
            rows = conn.execute("SELECT * FROM members WHERE is_active = 1 ORDER BY name").fetchall()
        else:
            rows = conn.execute("SELECT * FROM members ORDER BY name").fetchall()
    return [_row_to_member(r) for r in rows]


def search(keyword: str) -> list[Member]:
    with get_db() as conn:
        like = f"%{keyword}%"
        rows = conn.execute(
            "SELECT * FROM members WHERE is_active = 1 AND (name LIKE ? OR phone LIKE ? OR email LIKE ?) ORDER BY name",
            (like, like, like)
        ).fetchall()
    return [_row_to_member(r) for r in rows]


def update(member: Member) -> Member:
    member.update()
    with get_db() as conn:
        conn.execute(
            """UPDATE members SET name=?, phone=?, email=?, gender=?, date_of_birth=?,
               address=?, emergency_contact=?, updated_at=?, is_active=? WHERE id=?""",
            (member.name, member.phone, member.email, member.gender, member.date_of_birth,
             member.address, member.emergency_contact, member.updated_at.isoformat(),
             int(member.is_active), member.id)
        )
    return member


def delete(id: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE members SET is_active = 0, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), id)
        )
