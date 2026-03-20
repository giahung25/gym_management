# Báo cáo Kế hoạch & Việc cần làm — Gym Management System

**Ngày tạo:** 2026-03-19
**Dự án:** Gym Management System
**Trạng thái:** Đang phát triển

---

## 1. Tổng quan tiến độ hiện tại

### 1.1 Kiến trúc tổng thể

```
gym_management/
├── app/
│   ├── core/
│   │   ├── config.py          ✅ Hoàn thành
│   │   ├── database.py        ✅ Hoàn thành
│   │   └── security.py        ❌ Chưa implement
│   ├── models/                ✅ Hoàn thành
│   ├── repositories/          ✅ Hoàn thành
│   ├── services/
│   │   ├── member_svc.py      ✅ Hoàn thành
│   │   ├── membership_svc.py  ✅ Hoàn thành
│   │   ├── equipment_svc.py   ✅ Hoàn thành
│   │   ├── payment_svc.py     ❌ Stub trống
│   │   └── trainer_svc.py     ❌ Stub trống
│   └── api/                   ❌ Stub trống (không dùng)
├── gui/
│   ├── dashboard.py           ✅ Hoàn thành (kết nối DB thật)
│   ├── members.py             ✅ Hoàn thành
│   ├── memberships.py         ✅ Hoàn thành
│   ├── equipment.py           ✅ Hoàn thành
│   ├── reports.py             ✅ Hoàn thành
│   └── login.py               ❌ Chưa tạo
└── tests/                     ❌ Chưa có
```

### 1.2 Bảng tóm tắt trạng thái

| Layer | Module | Trạng thái | Ghi chú |
|-------|--------|:----------:|---------|
| **Core** | `config.py` | ✅ Xong | Settings, constants |
| **Core** | `database.py` | ✅ Xong | SQLite3 connection + 4 bảng schema |
| **Core** | `security.py` | ❌ Chưa làm | Auth, password hashing |
| **Models** | `base.py` | ✅ Xong | UUID, created_at, updated_at, is_active |
| **Models** | `member.py` | ⚠️ Thiếu | Thiếu field `photo` |
| **Models** | `membership.py` | ✅ Xong | MembershipPlan + MembershipSubscription |
| **Models** | `equipment.py` | ⚠️ Thiếu | Thiếu field `location` trong class |
| **Repositories** | `member_repo.py` | ✅ Xong | Full CRUD + search |
| **Repositories** | `membership_repo.py` | ✅ Xong | Full CRUD + expiring_soon |
| **Repositories** | `equipment_repo.py` | ✅ Xong | Full CRUD + filter by status/category |
| **Services** | `member_svc.py` | ✅ Xong | Validate, CRUD, stats |
| **Services** | `membership_svc.py` | ✅ Xong | Validate, subscribe, revenue stats, monthly revenue, plan stats |
| **Services** | `equipment_svc.py` | ✅ Xong | Validate, CRUD, summary |
| **Services** | `payment_svc.py` | ❌ Stub | Trống — chưa implement |
| **Services** | `trainer_svc.py` | ❌ Stub | Trống — chưa implement |
| **GUI** | `theme.py` | ✅ Xong | Design tokens: màu, font, spacing |
| **GUI** | `sidebar.py` | ✅ Xong | Navigation hoạt động đầy đủ |
| **GUI** | `header.py` | ✅ Xong | Search bar + avatar |
| **GUI** | `dashboard.py` | ✅ Xong | Kết nối đầy đủ DB: KPI, charts, packages, equipment |
| **GUI** | `members.py` | ✅ Xong | CRUD đầy đủ, search |
| **GUI** | `memberships.py` | ✅ Xong | Gói tập + đăng ký |
| **GUI** | `equipment.py` | ✅ Xong | CRUD + filter trạng thái |
| **GUI** | `reports.py` | ✅ Xong | KPI, thiết bị, gói sắp hết hạn |
| **GUI** | `login.py` | ❌ Chưa làm | Màn hình đăng nhập |
| **Tests** | `tests/` | ❌ Chưa làm | Không có test nào |

---

## 2. Bảng kế hoạch việc cần làm

### Ưu tiên 1 — CAO (làm ngay)

| # | Việc cần làm | File liên quan | Mô tả chi tiết |
|---|---|---|---|
| 1.1 | ~~**Kết nối Dashboard với dữ liệu thật**~~ ✅ **XONG** | `gui/dashboard.py`, `membership_svc.py` | Thêm `get_monthly_revenue()` và `get_plan_subscription_stats()` vào service. Dashboard: revenue chart, active growth chart, packages row, equipment row đều dùng dữ liệu thật từ DB. Hiển thị thông báo rỗng khi DB chưa có dữ liệu. |
| 1.2 | **Màn hình Login** | `gui/login.py`, `app/main.py` | Tạo màn hình đăng nhập với form username/password. Khi app khởi động, chuyển đến login thay vì dashboard. |
| 1.3 | **Implement security.py** | `app/core/security.py` | Thêm password hashing (dùng `hashlib` hoặc `bcrypt`), hàm `verify_password()`, tạo tài khoản admin mặc định khi `init_db()`. |
| 1.4 | **Thêm field `photo` vào Member** | `app/models/member.py` | Thêm `self.photo = photo` vào `__init__`. Cập nhật `member_repo.py` để lưu/đọc field này. |
| 1.5 | **Thêm field `location` vào Equipment** | `app/models/equipment.py` | Thêm `self.location = location` vào `__init__`. Hiện tại repo đang dùng `getattr()` để bypass — cần sửa đúng. |

---

### Ưu tiên 2 — TRUNG BÌNH (làm sau khi xong priority 1)

| # | Việc cần làm | File liên quan | Mô tả chi tiết |
|---|---|---|---|
| 2.1 | **Chi tiết hội viên — lịch sử gói tập** | `gui/members.py` | Thêm nút "Chi tiết" cho mỗi hội viên. Mở panel/dialog hiển thị danh sách subscription của hội viên đó qua `membership_repo.get_subscriptions_by_member(member_id)`. |
| 2.2 | **Widget "Sắp hết hạn" trên Dashboard** | `gui/dashboard.py` | Thêm bảng nhỏ ở dashboard hiển thị các gói tập sắp hết hạn trong 7 ngày (dùng `membership_repo.get_expiring_soon(days=7)`). |
| 2.3 | **Filter nâng cao trang Members** | `gui/members.py` | Thêm bộ lọc theo trạng thái subscription (active/expired), theo giới tính. |
| 2.4 | **Hủy đăng ký gói tập (Cancel)** | `gui/memberships.py`, `membership_svc.py` | Thêm nút "Hủy" cho từng subscription đang active. Gọi `sub.cancel()` và cập nhật DB. |
| 2.5 | **Thống kê doanh thu theo tháng** | `gui/reports.py` | Bổ sung biểu đồ doanh thu 6 tháng gần nhất (hiện chỉ có tổng). Query theo `created_at` nhóm theo tháng. |

---

### Ưu tiên 3 — THẤP (cải tiến & hoàn thiện)

| # | Việc cần làm | File liên quan | Mô tả chi tiết |
|---|---|---|---|
| 3.1 | **Xuất báo cáo CSV** | `gui/reports.py` | Thêm nút "Xuất CSV" để export danh sách hội viên, doanh thu. Dùng module `csv` của Python. |
| 3.2 | **Viết Tests** | `tests/` | Tạo thư mục `tests/`. Tối thiểu cần test: `test_member_svc.py`, `test_membership_svc.py`, `test_equipment_svc.py` — tập trung vào validate logic và business rules. |
| 3.3 | **Dọn dẹp stub không dùng** | `app/services/payment_svc.py`, `app/services/trainer_svc.py`, `app/api/` | Xóa các file stub trống không có kế hoạch implement trong tương lai gần để tránh gây nhầm lẫn về kiến trúc. |
| 3.4 | **Thông báo Toast / Snackbar** | Tất cả GUI screens | Thêm `page.snack_bar` để thông báo thành công/lỗi sau khi lưu, xóa dữ liệu thay vì chỉ đóng dialog. |
| 3.5 | **Upload ảnh hội viên** | `gui/members.py` | Sau khi đã thêm field `photo` vào model, implement chức năng chọn ảnh từ máy tính (dùng `ft.FilePicker`). |
| 3.6 | **Pagination cho bảng danh sách** | `gui/members.py`, `gui/memberships.py`, `gui/equipment.py` | Khi dữ liệu lớn, bảng sẽ bị quá dài. Thêm phân trang hoặc lazy load. |

---

## 3. Thứ tự thực hiện gợi ý

```
Tuần 1
├── [1.4] Thêm field photo vào Member model
├── [1.5] Thêm field location vào Equipment model
└── [1.1] ✅ Kết nối Dashboard với dữ liệu thật — XONG (2026-03-19)

Tuần 2
├── [1.3] Implement security.py (password hashing)
└── [1.2] Màn hình Login

Tuần 3
├── [2.1] Chi tiết hội viên — lịch sử gói tập
├── [2.2] Widget "Sắp hết hạn" trên Dashboard
└── [2.4] Hủy đăng ký gói tập

Tuần 4
├── [2.3] Filter nâng cao Members
├── [2.5] Thống kê doanh thu theo tháng
└── [3.4] Thông báo Toast / Snackbar

Tuần 5+
├── [3.2] Viết Tests
├── [3.1] Xuất báo cáo CSV
├── [3.5] Upload ảnh hội viên
├── [3.6] Pagination
└── [3.3] Dọn dẹp stub
```

---

## 4. Vấn đề kỹ thuật cần lưu ý

| Vấn đề | Chi tiết | Giải pháp |
|--------|----------|-----------|
| ~~**Dashboard mock data**~~ | ~~`gui/dashboard.py` hardcode số liệu, không phản ánh DB thật~~ | ✅ Đã fix — tất cả charts và sections dùng dữ liệu thật |
| **`Equipment.location` thiếu trong model** | `equipment_repo.py` dùng `getattr(eq, 'location', None)` — đây là workaround tạm | Thêm `location` vào `Equipment.__init__` |
| **`Member.photo` repo hardcode `None`** | `member_repo.py` luôn truyền `None` cho cột `photo` | Thêm field vào model, cập nhật repo |
| **Không có authentication** | App hiện tại không có bảo vệ — ai cũng vào được | Implement login screen + security.py |
| **Subscription `start_date` kiểu dữ liệu** | `membership_svc.subscribe_member()` nhận `datetime` nhưng `MembershipSubscription` dùng `date` — cần thống nhất | Chuẩn hóa về `date` hoặc `datetime` nhất quán |
| **Overlay dialog tích lũy** | Mỗi lần navigate sang màn hình mới, `page.overlay` có thể tích lũy dialog cũ | Xóa overlay khi navigate hoặc kiểm tra trước khi append |

---

## 5. Stack công nghệ

| Thành phần | Công nghệ |
|-----------|-----------|
| Ngôn ngữ | Python 3.10+ |
| GUI | Flet |
| Database | SQLite3 (không ORM) |
| Password hashing *(cần thêm)* | `hashlib` (SHA-256) hoặc `bcrypt` |
| Testing *(cần thêm)* | `pytest` |
| Export CSV *(cần thêm)* | `csv` (built-in) |

---

*Báo cáo này được tạo ngày 2026-03-19 dựa trên đọc toàn bộ source code hiện tại.*
