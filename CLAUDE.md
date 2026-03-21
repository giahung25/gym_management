# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Gym Management System — desktop app quản lý phòng gym (hội viên, gói tập, thiết bị).
- **GUI**: Flet (Python desktop UI)
- **Database**: SQLite3 (`data/gym_db.db`)
- **Language**: Python thuần, không dùng ORM

## Commands

```bash
# Cài dependencies
pip install -r requirements.txt

# Chạy ứng dụng
python app/main.py

# Chạy tests (khi đã có)
python -m pytest tests/
python -m pytest tests/test_foo.py::test_bar   # chạy 1 test cụ thể
```

## Architecture

```
app/
├── main.py              # Entry point: ft.app(target=main)
├── core/
│   ├── config.py        # Settings / env vars
│   ├── database.py      # SQLite3 connection + schema (chưa implement)
│   └── security.py      # Auth, password hashing (chưa implement)
├── models/              # Pure Python dataclasses (không dùng ORM)
│   ├── base.py          # BaseModel: id (UUID4), created_at, updated_at, is_active
│   ├── member.py        # Member(BaseModel)
│   ├── membership.py    # MembershipPlan + MembershipSubscription(BaseModel)
│   └── equipment.py     # Equipment(BaseModel)
├── services/            # Business logic (chưa implement)
├── api/                 # Controller layer / routes (chưa implement)
└── utils/               # Helpers (chưa implement)

gui/
├── theme.py             # Design tokens: màu sắc, font size, spacing
├── dashboard.py         # Dashboard screen — dùng mock data
└── components/
    ├── sidebar.py       # Sidebar(page, active_route) → ft.Container
    └── header.py        # Header(page) → ft.Container
```

## Key Design Decisions

**Models không kết nối DB**: Các model trong `app/models/` là pure Python objects, chưa có persistence. `app/core/database.py` vẫn còn trống — tầng data access cần được xây dựng.

**GUI dùng mock data**: `gui/dashboard.py` hiện render với dữ liệu hardcode. Khi database xong, cần kết nối services → dashboard.

**Layout pattern của Flet**: Toàn bộ app bọc trong `ft.Row([Sidebar, ft.Column([Header, content])])`. Sidebar width cố định `220px` (xem `gui/theme.py`). Content area dùng `ft.Column(..., scroll=ft.ScrollMode.AUTO)`.

**BaseModel.update()**: Chỉ cập nhật `updated_at`, không nhận kwargs. Khác với mô tả trong `doc/report_models.md` — khi cần update fields phải dùng `setattr` thủ công rồi gọi `self.update()`.

**Status constants**: Định nghĩa trực tiếp trên class (ví dụ `MembershipSubscription.STATUS_ACTIVE = "active"`, `Equipment.STATUS_WORKING = "working"`).

## Database Schema (planned — `data/gym_db.db`)

Theo `doc/note.txt`, 4 bảng chính cần implement:
- `members` — hội viên (id, name, phone, email, gender, date_of_birth, address, emergency_contact, photo)
- `membership_plans` — gói tập (id, name, duration_days, price, description)
- `subscriptions` — đăng ký gói (id, member_id FK, plan_id FK, price_paid, start_date, end_date, status)
- `equipment` — thiết bị (id, name, category, quantity, status, purchase_date, location, notes)

## GUI Screens (planned per `doc/note.txt`)

Đã làm: `dashboard.py`
Chưa làm: `login.py`, `members.py`, `memberships.py`, `equipment.py`

Thêm màn hình mới: tạo file trong `gui/`, import vào `app/main.py`, thêm nav item vào `gui/components/sidebar.py`.

# Quy tắc hoạt động của AI (AI Rules)

## Báo cáo công việc (Activity Logging)
- MỖI KHI bạn thực hiện bất kỳ thay đổi nào vào mã nguồn (thêm, sửa, xóa file), bạn PHẢI cập nhật hoặc tạo mới tệp `AI_REPORT.md`.
- Nội dung trong `AI_REPORT.md` cần bao gồm:
    - **Thời gian:** (Sử dụng lệnh `date` của hệ thống để lấy giờ chính xác).
    - **Các file đã tác động:** Danh sách các file.
    - **Tóm tắt thay đổi:** Giải thích ngắn gọn logic bạn đã sửa/thêm.
    - **Trạng thái Test:** Kết quả của lệnh chạy test (nếu có).
- Định dạng báo cáo: Sử dụng định dạng Markdown, thêm nội dung mới lên ĐẦU tệp để dễ theo dõi.

## Báo cáo tiến độ (Progress Reporting)
- Sau khi hoàn thành mỗi Ưu tiên (Priority) trong `doc/report_plan.md`, bạn PHẢI cập nhật file đó.
- Nội dung cập nhật bao gồm:
    - Đánh dấu ✅ cho các mục đã xong.
    - Ghi chú ngắn gọn về các thay đổi quan trọng (ví dụ: "Bỏ getattr() workaround", "Chuẩn hóa start_date").
    - Đánh giá lại các mục "Cần cải thiện" (nếu có).
- Mục tiêu: `report_plan.md` luôn phản ánh chính xác 100% trạng thái hiện tại của codebase.

## Không cần commit và push lên git khi chưa có yêu cầu không đưa presentation lên github

