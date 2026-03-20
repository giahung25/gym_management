from app.models.equipment import Equipment
from app.repositories import equipment_repo


def add_equipment(name: str, category: str, quantity: int = 1,
                  purchase_date=None, notes: str = None, location: str = None) -> Equipment:
    if not name or not name.strip():
        raise ValueError("Tên thiết bị không được để trống")
    if not category or not category.strip():
        raise ValueError("Loại thiết bị không được để trống")
    eq = Equipment(
        name=name.strip(),
        category=category.strip(),
        quantity=quantity,
        purchase_date=purchase_date,
        notes=notes,
    )
    eq.location = location
    return equipment_repo.create(eq)


def update_equipment(eq: Equipment, **kwargs) -> Equipment:
    for k, v in kwargs.items():
        setattr(eq, k, v)
    return equipment_repo.update(eq)


def get_equipment_summary() -> dict:
    all_eq = equipment_repo.get_all(active_only=True)
    working = sum(1 for e in all_eq if e.status == Equipment.STATUS_WORKING)
    broken = sum(1 for e in all_eq if e.status == Equipment.STATUS_BROKEN)
    maintenance = sum(1 for e in all_eq if e.status == Equipment.STATUS_MAINTENANCE)
    categories = {}
    for e in all_eq:
        categories[e.category] = categories.get(e.category, 0) + 1
    return {
        "total": len(all_eq),
        "working": working,
        "broken": broken,
        "maintenance": maintenance,
        "categories": categories,
    }
