import re
from datetime import datetime
from app.models.member import Member
from app.repositories import member_repo


def _validate(name: str, phone: str, email: str = None):
    if not name or not name.strip():
        raise ValueError("Tên hội viên không được để trống")
    if not phone or not phone.strip():
        raise ValueError("Số điện thoại không được để trống")
    if not re.fullmatch(r"[0-9+\-\s]{7,15}", phone.strip()):
        raise ValueError("Số điện thoại không hợp lệ")
    if email and not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email.strip()):
        raise ValueError("Email không hợp lệ")


def register_member(name: str, phone: str, email: str = None, gender: str = None,
                    date_of_birth=None, address: str = None,
                    emergency_contact: str = None) -> Member:
    _validate(name, phone, email)
    member = Member(
        name=name.strip(),
        phone=phone.strip(),
        email=email.strip() if email else None,
        gender=gender,
        date_of_birth=date_of_birth,
        address=address,
        emergency_contact=emergency_contact,
    )
    return member_repo.create(member)


def update_member(member: Member) -> Member:
    """Validate rồi lưu member đã được mutate trực tiếp từ caller.

    Caller tự set các field trước khi gọi hàm này:
        member.name = "Tên mới"
        member_svc.update_member(member)
    """
    _validate(member.name, member.phone, member.email)
    return member_repo.update(member)


def get_member_stats() -> dict:
    all_members = member_repo.get_all(active_only=False)
    active = [m for m in all_members if m.is_active]
    now = datetime.now()
    new_this_month = [
        m for m in active
        if m.created_at.year == now.year and m.created_at.month == now.month
    ]
    return {
        "total": len(all_members),
        "active": len(active),
        "new_this_month": len(new_this_month),
    }
