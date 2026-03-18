# Báo cáo chi tiết: Tầng Models — Gym Management System

**Ngày tạo:** 2026-03-18
**Phạm vi:** `app/models/`
**Dự án:** Gym Management System

---

## 1. Tổng quan dự án

| Mục | Chi tiết |
|-----|----------|
| Tên dự án | Gym Management System |
| Ngôn ngữ | Python (thuần, không dùng ORM) |
| Database | SQLite3 |
| GUI Framework | Flet |
| Phạm vi báo cáo | `app/models/` |

---

## 2. Cấu trúc tầng Models

```
app/
└── models/
    ├── __init__.py          # Export tất cả models
    ├── base.py              # BaseModel — lớp nền chung
    ├── member.py            # Member — hội viên
    ├── membership.py        # MembershipPlan + MembershipSubscription
    └── equipment.py         # Equipment — thiết bị
```

---

## 3. Chi tiết từng file

### 3.1 `app/models/base.py` — BaseModel

**Mô tả:** Lớp nền (base class) mà tất cả các model khác kế thừa. Cung cấp các field chung và method cơ bản.

#### Bug đã phát hiện và sửa
- **Lỗi:** Các method `update()`, `delete()`, `to_dict()` bị định nghĩa **lồng bên trong `__init__()`** thay vì ở cấp class → các method này không thể gọi từ bên ngoài như instance method bình thường.
- **Sửa:** Đưa toàn bộ method ra cấp class đúng chuẩn Python.
- **Lỗi thứ hai:** Tên field `is_activate` (sai) → đổi thành `is_active` để nhất quán với Python convention và các model con.

#### Fields

| Field | Kiểu | Mô tả |
|-------|------|--------|
| `id` | `str` (UUID4) | Khóa chính, tự sinh khi tạo |
| `created_at` | `datetime` | Thời điểm tạo bản ghi |
| `updated_at` | `datetime` | Thời điểm cập nhật gần nhất |
| `is_active` | `bool` | Trạng thái hoạt động (mặc định `True`) |

#### Methods

| Method | Tham số | Trả về | Mô tả |
|--------|---------|--------|--------|
| `__init__()` | — | — | Khởi tạo id (UUID), created_at, updated_at, is_active |
| `update(**kwargs)` | `**kwargs` | `None` | Cập nhật các field được truyền vào, tự cập nhật `updated_at` |
| `delete()` | — | `None` | Soft delete: đặt `is_active = False`, cập nhật `updated_at` |
| `to_dict()` | — | `dict` | Chuyển object sang dict; các field `datetime` được chuyển sang ISO string |

#### Code tham khảo

```python
class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.is_active = True

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def delete(self):
        self.is_active = False
        self.updated_at = datetime.now()

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
```

---

### 3.2 `app/models/member.py` — Member

**Mô tả:** Đại diện cho một hội viên của phòng gym. Kế thừa `BaseModel`.

#### Fields bổ sung so với phiên bản gốc
Ban đầu model chỉ có `name` và `phone`. Đã bổ sung thêm các field:
- `email`
- `gender`
- `date_of_birth`
- `address`
- `emergency_contact`

#### Fields đầy đủ

| Field | Kiểu | Mặc định | Mô tả |
|-------|------|----------|--------|
| `id` | `str` | UUID4 (từ BaseModel) | Khóa chính |
| `name` | `str` | — | Họ tên hội viên |
| `phone` | `str` | — | Số điện thoại |
| `email` | `str` | `""` | Địa chỉ email |
| `gender` | `str` | `""` | Giới tính (`male` / `female` / `other`) |
| `date_of_birth` | `str` | `""` | Ngày sinh (ISO format) |
| `address` | `str` | `""` | Địa chỉ |
| `emergency_contact` | `str` | `""` | Liên hệ khẩn cấp |
| `created_at` | `datetime` | now() (từ BaseModel) | Ngày tạo |
| `updated_at` | `datetime` | now() (từ BaseModel) | Ngày cập nhật |
| `is_active` | `bool` | `True` (từ BaseModel) | Trạng thái hoạt động |

#### Code tham khảo

```python
class Member(BaseModel):
    def __init__(self, name: str, phone: str, email: str = "",
                 gender: str = "", date_of_birth: str = "",
                 address: str = "", emergency_contact: str = ""):
        super().__init__()
        self.name = name
        self.phone = phone
        self.email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.address = address
        self.emergency_contact = emergency_contact
```

---

### 3.3 `app/models/membership.py` — MembershipPlan & MembershipSubscription

**Mô tả:** Gồm hai class liên quan đến gói tập và đăng ký của hội viên.

---

#### 3.3.1 MembershipPlan

Đại diện cho một gói tập (ví dụ: "Gói 1 tháng", "Gói 3 tháng").

| Field | Kiểu | Mô tả |
|-------|------|--------|
| `id` | `str` | UUID4 (từ BaseModel) |
| `name` | `str` | Tên gói tập |
| `duration_days` | `int` | Số ngày hiệu lực |
| `price` | `float` | Giá gói tập |
| `description` | `str` | Mô tả (tùy chọn) |

```python
class MembershipPlan(BaseModel):
    def __init__(self, name: str, duration_days: int,
                 price: float, description: str = ""):
        super().__init__()
        self.name = name
        self.duration_days = duration_days
        self.price = price
        self.description = description
```

---

#### 3.3.2 MembershipSubscription

Đại diện cho một lần đăng ký gói tập của hội viên. Kế thừa `BaseModel`.

| Field | Kiểu | Mô tả |
|-------|------|--------|
| `id` | `str` | UUID4 (từ BaseModel) |
| `member_id` | `str` | FK → Member.id |
| `plan_id` | `str` | FK → MembershipPlan.id |
| `price_paid` | `float` | Giá thực tế đã trả |
| `start_date` | `date` | Ngày bắt đầu |
| `end_date` | `date` | Ngày kết thúc (tự tính từ plan) |
| `status` | `str` | `active` / `expired` / `cancelled` |

#### Status Constants

```python
STATUS_ACTIVE    = "active"
STATUS_EXPIRED   = "expired"
STATUS_CANCELLED = "cancelled"
```

#### Methods

| Method | Tham số | Trả về | Mô tả |
|--------|---------|--------|--------|
| `is_expired()` | — | `bool` | Trả về `True` nếu `end_date < today` |
| `days_remaining()` | — | `int` | Số ngày còn lại (0 nếu đã hết hạn) |
| `cancel()` | — | `None` | Đặt status = `cancelled`, cập nhật `updated_at` |
| `refresh_status()` | — | `None` | Tự động cập nhật status dựa trên ngày hiện tại |

```python
class MembershipSubscription(BaseModel):
    def __init__(self, member_id: str, plan_id: str,
                 price_paid: float, start_date: date,
                 duration_days: int):
        super().__init__()
        self.member_id = member_id
        self.plan_id = plan_id
        self.price_paid = price_paid
        self.start_date = start_date
        self.end_date = start_date + timedelta(days=duration_days)
        self.status = STATUS_ACTIVE

    def is_expired(self) -> bool:
        return date.today() > self.end_date

    def days_remaining(self) -> int:
        delta = self.end_date - date.today()
        return max(0, delta.days)

    def cancel(self):
        self.status = STATUS_CANCELLED
        self.updated_at = datetime.now()

    def refresh_status(self):
        if self.status != STATUS_CANCELLED:
            if self.is_expired():
                self.status = STATUS_EXPIRED
            else:
                self.status = STATUS_ACTIVE
```

---

### 3.4 `app/models/equipment.py` — Equipment

**Mô tả:** Đại diện cho một thiết bị trong phòng gym. Kế thừa `BaseModel`.

#### Fields

| Field | Kiểu | Mặc định | Mô tả |
|-------|------|----------|--------|
| `id` | `str` | UUID4 (từ BaseModel) | Khóa chính |
| `name` | `str` | — | Tên thiết bị |
| `category` | `str` | `""` | Danh mục (ví dụ: cardio, strength) |
| `quantity` | `int` | `1` | Số lượng |
| `status` | `str` | `working` | Trạng thái thiết bị |
| `purchase_date` | `str` | `""` | Ngày mua (ISO format) |
| `notes` | `str` | `""` | Ghi chú |

#### Status Constants

```python
STATUS_WORKING     = "working"
STATUS_BROKEN      = "broken"
STATUS_MAINTENANCE = "maintenance"
```

#### Methods

| Method | Tham số | Trả về | Mô tả |
|--------|---------|--------|--------|
| `mark_broken()` | — | `None` | Đặt status = `broken`, cập nhật `updated_at` |
| `mark_maintenance()` | — | `None` | Đặt status = `maintenance`, cập nhật `updated_at` |
| `mark_working()` | — | `None` | Đặt status = `working`, cập nhật `updated_at` |
| `is_available()` | — | `bool` | Trả về `True` nếu status == `working` |

```python
class Equipment(BaseModel):
    def __init__(self, name: str, category: str = "",
                 quantity: int = 1, purchase_date: str = "",
                 notes: str = ""):
        super().__init__()
        self.name = name
        self.category = category
        self.quantity = quantity
        self.status = STATUS_WORKING
        self.purchase_date = purchase_date
        self.notes = notes

    def mark_broken(self):
        self.status = STATUS_BROKEN
        self.updated_at = datetime.now()

    def mark_maintenance(self):
        self.status = STATUS_MAINTENANCE
        self.updated_at = datetime.now()

    def mark_working(self):
        self.status = STATUS_WORKING
        self.updated_at = datetime.now()

    def is_available(self) -> bool:
        return self.status == STATUS_WORKING
```

---

### 3.5 `app/models/__init__.py` — Export

**Mô tả:** File export tập trung để các module khác import model qua `app.models`.

```python
from app.models.base import BaseModel
from app.models.member import Member
from app.models.membership import MembershipPlan, MembershipSubscription
from app.models.equipment import Equipment

__all__ = [
    "BaseModel",
    "Member",
    "MembershipPlan",
    "MembershipSubscription",
    "Equipment",
]
```

---

## 4. Điểm còn thiếu so với `note.txt`

| Field / File thiếu | Lý do | Ưu tiên |
|---------------------|-------|---------|
| `member.photo` | Field ảnh hội viên có trong yêu cầu `note.txt` nhưng chưa được thêm | Trung bình |
| `equipment.location` | Field vị trí thiết bị có trong yêu cầu `note.txt` nhưng chưa được thêm | Thấp |
| `app/core/database.py` | SQLite3 schema và kết nối chưa được xây dựng | **Cao** |
| Validation | Chưa có kiểm tra định dạng số điện thoại, ngày tháng, email | Trung bình |

---

## 5. Phần chưa làm (ngoài phạm vi lần này)

| Module | Mô tả |
|--------|--------|
| `app/core/database.py` | Tạo kết nối SQLite3, định nghĩa schema các bảng (`members`, `membership_plans`, `subscriptions`, `equipment`) |
| `app/services/` | Business logic: tìm kiếm, lọc, xử lý nghiệp vụ |
| `app/api/` hoặc `app/repositories/` | Data access layer — CRUD với SQLite3 |
| `gui/` | Giao diện Flet — không đụng đến trong phạm vi này |

---

## 6. Tóm tắt

| File | Class(es) | Trạng thái |
|------|-----------|------------|
| `base.py` | `BaseModel` | Hoàn thành (đã sửa bug indent + is_active) |
| `member.py` | `Member` | Hoàn thành (thiếu `photo`) |
| `membership.py` | `MembershipPlan`, `MembershipSubscription` | Hoàn thành |
| `equipment.py` | `Equipment` | Hoàn thành (thiếu `location`) |
| `__init__.py` | — | Hoàn thành |
