from app.core.database import get_db
from app.models.equipment import Equipment
from datetime import datetime


def _row_to_equipment(row) -> Equipment:
    e = Equipment.__new__(Equipment)
    e.id = row["id"]
    e.name = row["name"]
    e.category = row["category"]
    e.quantity = row["quantity"]
    e.status = row["status"]
    e.purchase_date = row["purchase_date"]
    e.location = row["location"]
    e.notes = row["notes"]
    e.created_at = datetime.fromisoformat(row["created_at"])
    e.updated_at = datetime.fromisoformat(row["updated_at"])
    e.is_active = bool(row["is_active"])
    return e


def create(equipment: Equipment) -> Equipment:
    with get_db() as conn:
        conn.execute(
            """INSERT INTO equipment (id, name, category, quantity, status, purchase_date,
               location, notes, created_at, updated_at, is_active)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (equipment.id, equipment.name, equipment.category, equipment.quantity,
             equipment.status, equipment.purchase_date,
             equipment.location, equipment.notes,
             equipment.created_at.isoformat(), equipment.updated_at.isoformat(),
             int(equipment.is_active))
        )
    return equipment


def get_by_id(id: str) -> Equipment | None:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM equipment WHERE id = ?", (id,)).fetchone()
    return _row_to_equipment(row) if row else None


def get_all(active_only: bool = True) -> list[Equipment]:
    with get_db() as conn:
        if active_only:
            rows = conn.execute("SELECT * FROM equipment WHERE is_active = 1 ORDER BY name").fetchall()
        else:
            rows = conn.execute("SELECT * FROM equipment ORDER BY name").fetchall()
    return [_row_to_equipment(r) for r in rows]


def get_by_status(status: str) -> list[Equipment]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM equipment WHERE is_active = 1 AND status = ? ORDER BY name", (status,)
        ).fetchall()
    return [_row_to_equipment(r) for r in rows]


def get_by_category(category: str) -> list[Equipment]:
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM equipment WHERE is_active = 1 AND category = ? ORDER BY name", (category,)
        ).fetchall()
    return [_row_to_equipment(r) for r in rows]


def update(equipment: Equipment) -> Equipment:
    equipment.update()
    with get_db() as conn:
        conn.execute(
            """UPDATE equipment SET name=?, category=?, quantity=?, status=?,
               purchase_date=?, location=?, notes=?, updated_at=?, is_active=? WHERE id=?""",
            (equipment.name, equipment.category, equipment.quantity, equipment.status,
             equipment.purchase_date, equipment.location, equipment.notes,
             equipment.updated_at.isoformat(), int(equipment.is_active), equipment.id)
        )
    return equipment


def delete(id: str):
    with get_db() as conn:
        conn.execute(
            "UPDATE equipment SET is_active = 0, updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), id)
        )
