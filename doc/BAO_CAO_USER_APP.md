# BÁO CÁO THIẾT KẾ APP NGƯỜI DÙNG
## Hệ thống quản lý phòng gym — GymFit Member App

**Ngày lập:** 01/04/2026
**Trạng thái:** Kế hoạch — chờ duyệt để triển khai

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1 Bối cảnh
Hệ thống hiện tại (`GymAdmin`) chỉ phục vụ **quản trị viên** phòng gym. Hội viên và huấn luyện viên không có cách nào tự tra cứu thông tin, đăng ký gói tập hay theo dõi thông báo mà không cần nhờ admin.

### 1.2 Mục tiêu
Xây dựng app riêng **GymFit Member App** dành cho:
- **Hội viên**: tự đăng nhập, xem thông tin gói tập, đăng ký/gia hạn, xem lịch sử
- **Huấn luyện viên (HLV)**: xem danh sách học viên, lịch dạy

### 1.3 Nền tảng
- **Framework:** Flet (Desktop) — nhất quán với app admin hiện có
- **Database:** SQLite3 (dùng chung file `data/gym_db.db`)
- **Ngôn ngữ:** Python 3.10+
- **Entry point riêng:** `python app/user_main.py`

---

## 2. YÊU CẦU CHỨC NĂNG (User Stories)

### Hội viên
| ID | Mô tả |
|----|-------|
| US-01 | Là hội viên, tôi muốn đăng nhập bằng SĐT + PIN để vào app |
| US-02 | Là hội viên, tôi muốn xem gói tập đang active và số ngày còn lại |
| US-03 | Là hội viên, tôi muốn xem thông tin cá nhân (tên, email, địa chỉ) |
| US-04 | Là hội viên, tôi muốn đổi PIN đăng nhập |
| US-05 | Là hội viên, tôi muốn xem danh sách các gói tập và đăng ký/gia hạn |
| US-06 | Là hội viên, tôi muốn xem lịch sử tất cả gói tập đã đăng ký |
| US-07 | Là hội viên, tôi muốn nhận thông báo khi gói tập sắp hết hạn (≤7 ngày) |

### Huấn luyện viên
| ID | Mô tả |
|----|-------|
| US-08 | Là HLV, tôi muốn đăng nhập bằng SĐT + PIN để vào app |
| US-09 | Là HLV, tôi muốn xem thông tin cá nhân và chuyên môn |
| US-10 | Là HLV, tôi muốn xem danh sách học viên của mình |

---

## 3. KIẾN TRÚC HỆ THỐNG

### 3.1 Tổng quan
```
┌─────────────────────────────────────────────────────────┐
│                     NGƯỜI DÙNG                          │
│           Hội viên              Huấn luyện viên         │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────────────────────────────────────┐
│              GymFit Member App  (app/user_main.py)       │
│  ┌─────────────────────────────────────────────────────┐ │
│  │                GUI Layer (gui/user/)                │ │
│  │  user_login → user_dashboard / trainer_dashboard   │ │
│  │  user_profile | user_membership | user_history     │ │
│  │  user_notifications | trainer_dashboard            │ │
│  └───────────────────────┬─────────────────────────────┘ │
│                          │                               │
│  ┌───────────────────────▼─────────────────────────────┐ │
│  │             Services Layer (app/services/)          │ │
│  │  auth_svc | notification_svc | membership_svc      │ │
│  │  member_svc | trainer_svc                          │ │
│  └───────────────────────┬─────────────────────────────┘ │
│                          │                               │
│  ┌───────────────────────▼─────────────────────────────┐ │
│  │          Repositories Layer (app/repositories/)     │ │
│  │  member_repo | trainer_repo | notification_repo    │ │
│  │  membership_repo                                   │ │
│  └───────────────────────┬─────────────────────────────┘ │
│                          │                               │
│  ┌───────────────────────▼─────────────────────────────┐ │
│  │           Database: data/gym_db.db (SQLite)         │ │
│  └─────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────┘

       GymAdmin App (app/main.py) — KHÔNG bị ảnh hưởng
```

### 3.2 Cấu trúc thư mục (file mới)
```
gym_management/
├── app/
│   ├── user_main.py                 ← Entry point user app
│   ├── models/
│   │   ├── trainer.py               ← Model HLV
│   │   └── notification.py          ← Model Thông báo
│   ├── repositories/
│   │   ├── trainer_repo.py          ← CRUD HLV
│   │   └── notification_repo.py     ← CRUD Thông báo
│   ├── services/
│   │   ├── auth_svc.py              ← Xác thực member/trainer
│   │   ├── trainer_svc.py           ← Logic HLV (cập nhật)
│   │   └── notification_svc.py      ← Quản lý thông báo
│   └── core/
│       └── database.py              ← Cập nhật: thêm bảng mới
└── gui/
    └── user/
        ├── user_login.py
        ├── user_dashboard.py
        ├── user_profile.py
        ├── user_membership.py
        ├── user_history.py
        ├── user_notifications.py
        ├── trainer_dashboard.py
        └── components/
            └── user_sidebar.py
```

---

## 4. THIẾT KẾ DATABASE

### 4.1 Thay đổi bảng `members` (hiện có)
Thêm 1 cột:
```sql
ALTER TABLE members ADD COLUMN pin TEXT NOT NULL DEFAULT '000000';
-- PIN 6 chữ số dùng để đăng nhập, mặc định là 000000
-- Admin đặt PIN ban đầu khi tạo hội viên
```

### 4.2 Bảng mới: `trainers`
```sql
CREATE TABLE trainers (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,        -- Họ tên HLV
    phone           TEXT NOT NULL,        -- SĐT (dùng để đăng nhập)
    email           TEXT,
    specialization  TEXT,                 -- Chuyên môn: "Yoga", "Gym", "Boxing"...
    pin             TEXT NOT NULL DEFAULT '000000',
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    is_active       INTEGER NOT NULL DEFAULT 1
);
```

### 4.3 Bảng mới: `notifications`
```sql
CREATE TABLE notifications (
    id          TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL,    -- ID hội viên hoặc HLV
    user_type   TEXT NOT NULL,    -- 'member' hoặc 'trainer'
    title       TEXT NOT NULL,    -- Tiêu đề
    message     TEXT NOT NULL,    -- Nội dung
    is_read     INTEGER NOT NULL DEFAULT 0,  -- 0=chưa đọc, 1=đã đọc
    created_at  TEXT NOT NULL
);
```

---

## 5. THIẾT KẾ UI/UX — WIREFRAME TỪNG MÀN HÌNH

### 5.1 Màn hình Đăng nhập (`user_login.py`)
```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║              🏋️  GymFit Member App                   ║
║                                                      ║
║         [ Hội viên ]    [ Huấn luyện viên ]          ║
║         ─────────────────────────────────            ║
║                                                      ║
║         Số điện thoại                                ║
║         ┌──────────────────────────────┐             ║
║         │  0901234567                  │             ║
║         └──────────────────────────────┘             ║
║                                                      ║
║         Mã PIN (6 số)                                ║
║         ┌──────────────────────────────┐             ║
║         │  ● ● ● ● ● ●                 │             ║
║         └──────────────────────────────┘             ║
║                                                      ║
║              [ ĐĂNG NHẬP ]                           ║
║                                                      ║
║         ⚠ Lần đầu đăng nhập dùng PIN: 000000        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

### 5.2 Dashboard Hội viên (`user_dashboard.py`)
```
╔══════════════════════════════════════════════════════════════╗
║  [≡] GymFit                              Xin chào, Nguyễn A ║
╠════════╦═════════════════════════════════════════════════════╣
║        ║                                                     ║
║ Trang  ║   👤 Nguyễn Văn A                                   ║
║ chủ    ║   📞 0901234567                                     ║
║        ║                                                     ║
║ Thông  ║   ┌─────────────────────────────────────────────┐   ║
║ tin    ║   │  GÓI TẬP ĐANG ACTIVE                        │   ║
║        ║   │  Gói 3 tháng                                │   ║
║ Gói    ║   │  Bắt đầu: 01/03/2026                        │   ║
║ tập    ║   │  Hết hạn: 01/06/2026    [████████░░] 60%    │   ║
║        ║   │  ⏳ Còn lại: 61 ngày                         │   ║
║ Lịch   ║   └─────────────────────────────────────────────┘   ║
║ sử     ║                                                     ║
║        ║   ┌───────────┐  ┌───────────┐  ┌──────────────┐   ║
║ Thông  ║   │ Gia hạn   │  │ Lịch sử  │  │ 🔔 Thông báo │   ║
║ báo 🔴2║   │ gói tập   │  │ thanh toán│  │    (2 mới)   │   ║
║        ║   └───────────┘  └───────────┘  └──────────────┘   ║
║ Đăng   ║                                                     ║
║ xuất   ║                                                     ║
╚════════╩═════════════════════════════════════════════════════╝
```

### 5.3 Thông tin cá nhân (`user_profile.py`)
```
╔══════════════════════════════════════════════════════════════╗
║  [≡] GymFit                                  Thông tin      ║
╠════════╦═════════════════════════════════════════════════════╣
║        ║                                                     ║
║ ...    ║   THÔNG TIN CÁ NHÂN                                 ║
║        ║   ┌─────────────────────────────────────────────┐   ║
║        ║   │  Họ tên:    Nguyễn Văn A                    │   ║
║        ║   │  SĐT:       0901234567                      │   ║
║        ║   │  Email:     nguyen@email.com                 │   ║
║        ║   │  Giới tính: Nam                              │   ║
║        ║   │  Ngày sinh: 15/01/2000                      │   ║
║        ║   │  Địa chỉ:  123 Đường ABC, Q.1, TP.HCM       │   ║
║        ║   └─────────────────────────────────────────────┘   ║
║        ║                                                     ║
║        ║   ĐỔI MÃ PIN                                        ║
║        ║   PIN hiện tại: [______]                            ║
║        ║   PIN mới:      [______]                            ║
║        ║   Xác nhận PIN: [______]                            ║
║        ║                     [ Lưu PIN mới ]                 ║
║        ║                                                     ║
╚════════╩═════════════════════════════════════════════════════╝
```

### 5.4 Gói tập & Đăng ký (`user_membership.py`)
```
╔══════════════════════════════════════════════════════════════╗
║  [≡] GymFit                                    Gói tập      ║
╠════════╦═════════════════════════════════════════════════════╣
║        ║  [ Gói hiện tại ]  [ Đăng ký / Gia hạn ]           ║
║        ║  ─────────────────────────────────────────          ║
║        ║                                                     ║
║  TAB 1 ║  TRẠNG THÁI GÓI TẬP                                 ║
║        ║  ┌─────────────────────────────────────────────┐   ║
║        ║  │  Gói 3 tháng    ● ĐANG HOẠT ĐỘNG            │   ║
║        ║  │  [████████████░░░░░░░░] 60% đã dùng         │   ║
║        ║  │  Ngày bắt đầu: 01/03/2026                   │   ║
║        ║  │  Ngày hết hạn: 01/06/2026                   │   ║
║        ║  │  Còn lại: 61 ngày                           │   ║
║        ║  │  Giá đã thanh toán: 1,200,000 đ             │   ║
║        ║  └─────────────────────────────────────────────┘   ║
║        ║                                                     ║
║  TAB 2 ║  CHỌN GÓI TẬP                                       ║
║        ║  ┌────────────┐ ┌────────────┐ ┌────────────┐      ║
║        ║  │ Gói 1 tháng│ │Gói 3 tháng │ │Gói 1 năm   │     ║
║        ║  │  30 ngày   │ │  90 ngày   │ │  365 ngày  │      ║
║        ║  │  500,000 đ │ │ 1,200,000 đ│ │ 4,000,000 đ│      ║
║        ║  │ [Đăng ký]  │ │ [Đăng ký]  │ │ [Đăng ký]  │     ║
║        ║  └────────────┘ └────────────┘ └────────────┘      ║
║        ║  * Sau khi đăng ký, admin sẽ xác nhận thanh toán   ║
╚════════╩═════════════════════════════════════════════════════╝
```

### 5.5 Lịch sử (`user_history.py`)
```
╔══════════════════════════════════════════════════════════════╗
║  [≡] GymFit                                   Lịch sử       ║
╠════════╦═════════════════════════════════════════════════════╣
║        ║  Năm: [2026 ▼]   Tháng: [Tất cả ▼]                 ║
║        ║                                                     ║
║        ║  ┌──────────────┬──────────┬──────────┬──────────┐  ║
║        ║  │ Gói tập      │ Bắt đầu  │ Hết hạn  │ Trạng    │  ║
║        ║  │              │          │          │ thái     │  ║
║        ║  ├──────────────┼──────────┼──────────┼──────────┤  ║
║        ║  │ Gói 3 tháng  │01/03/2026│01/06/2026│● Active  │  ║
║        ║  │ Gói 1 tháng  │01/12/2025│01/01/2026│○ Hết hạn │  ║
║        ║  │ Gói 3 tháng  │01/09/2025│01/12/2025│○ Hết hạn │  ║
║        ║  └──────────────┴──────────┴──────────┴──────────┘  ║
╚════════╩═════════════════════════════════════════════════════╝
```

### 5.6 Thông báo (`user_notifications.py`)
```
╔══════════════════════════════════════════════════════════════╗
║  [≡] GymFit                                  Thông báo      ║
╠════════╦═════════════════════════════════════════════════════╣
║        ║  [ Đánh dấu tất cả đã đọc ]                        ║
║        ║                                                     ║
║        ║  🔴 ┌─────────────────────────────────────────┐     ║
║        ║     │ Gói tập sắp hết hạn!              Hôm nay│    ║
║        ║     │ Gói 3 tháng của bạn còn 7 ngày nữa      │    ║
║        ║     │ sẽ hết hạn. Hãy gia hạn sớm.            │    ║
║        ║     └─────────────────────────────────────────┘     ║
║        ║                                                     ║
║        ║  ✅ ┌─────────────────────────────────────────┐     ║
║        ║     │ Đăng ký thành công                01/03 │    ║
║        ║     │ Bạn đã đăng ký thành công Gói 3 tháng. │    ║
║        ║     └─────────────────────────────────────────┘     ║
╚════════╩═════════════════════════════════════════════════════╝
```

### 5.7 Dashboard HLV (`trainer_dashboard.py`)
```
╔══════════════════════════════════════════════════════════════╗
║  [≡] GymFit                            Xin chào, Trần HLV   ║
╠════════════╦═════════════════════════════════════════════════╣
║            ║                                                 ║
║  Trang chủ ║  👨‍🏫 Trần Văn Huấn                               ║
║            ║  Chuyên môn: Gym & Fitness                      ║
║  Học viên  ║  📞 0909123456                                  ║
║            ║                                                 ║
║  Đăng xuất ║  DANH SÁCH HỌC VIÊN (12 người)                  ║
║            ║  ┌────────────────────────────────────────┐     ║
║            ║  │ Tên            │ SĐT         │ Gói tập │    ║
║            ║  ├────────────────┼─────────────┼─────────┤    ║
║            ║  │ Nguyễn Văn A   │ 0901234567  │ 3 tháng │    ║
║            ║  │ Trần Thị B     │ 0912345678  │ 1 năm   │    ║
║            ║  │ ...            │ ...         │ ...     │    ║
║            ║  └────────────────────────────────────────┘     ║
╚════════════╩═════════════════════════════════════════════════╝
```

---

## 6. LUỒNG NGƯỜI DÙNG (User Flow)

### 6.1 Luồng Hội viên
```
Mở app
  │
  ▼
[Màn hình đăng nhập]
  │ Chọn "Hội viên"
  │ Nhập SĐT + PIN → Xác thực auth_svc.login_member()
  │
  ├─ Sai → Hiện lỗi "SĐT hoặc PIN không đúng"
  │
  └─ Đúng ──────────────────────────────────────────────────┐
                                                            ▼
                                               [Dashboard hội viên]
                                                      │
                    ┌─────────────────────────────────┼───────────────────┐
                    ▼                                 ▼                   ▼
           [Thông tin cá nhân]              [Gói tập]              [Lịch sử]
                    │                           │
                    └── Đổi PIN                 ├── Tab: Gói hiện tại
                                                └── Tab: Đăng ký mới
                                                         │
                                                   Chọn gói → Xác nhận
                                                         │
                                              Tạo subscription "pending"
                                                (Admin xác nhận thanh toán)
```

### 6.2 Luồng HLV
```
Mở app
  │
  ▼
[Màn hình đăng nhập] → Chọn "Huấn luyện viên" → Nhập SĐT + PIN
  │
  └─ Đúng → [Dashboard HLV] → Xem danh sách học viên
```

### 6.3 Luồng thông báo tự động
```
Mỗi lần hội viên đăng nhập:
  auth_svc.login_member()
        │
        ▼
  notification_svc.check_expiring_subscriptions(member_id)
        │
        ├── Gói còn ≤ 7 ngày và chưa có thông báo hôm nay
        │         → Tạo thông báo "Gói tập sắp hết hạn"
        │
        └── Gói đã hết hạn
                  → Tạo thông báo "Gói tập đã hết hạn, hãy gia hạn"
```

---

## 7. DANH SÁCH FILES CẦN TRIỂN KHAI

### Files cần tạo mới (16 files)
| STT | File | Mô tả |
|-----|------|-------|
| 1 | `app/models/trainer.py` | Class Trainer: name, phone, email, specialization, pin |
| 2 | `app/models/notification.py` | Class Notification: user_id, user_type, title, message, is_read |
| 3 | `app/repositories/trainer_repo.py` | CRUD trainer: create, get_by_id, get_by_phone, get_all, update, delete |
| 4 | `app/repositories/notification_repo.py` | CRUD notification: create, get_by_user, mark_read, get_unread_count |
| 5 | `app/services/auth_svc.py` | login_member(), login_trainer(), change_pin() |
| 6 | `app/services/notification_svc.py` | create_notification(), check_expiring_subscriptions() |
| 7 | `app/user_main.py` | Entry point: khởi tạo Flet app, window 1100×700, route đến UserLogin |
| 8 | `gui/user/__init__.py` | Package init |
| 9 | `gui/user/components/__init__.py` | Package init |
| 10 | `gui/user/components/user_sidebar.py` | Sidebar với menu theo role (member/trainer) |
| 11 | `gui/user/user_login.py` | Màn hình đăng nhập, toggle member/trainer |
| 12 | `gui/user/user_dashboard.py` | Dashboard: ảnh, tên, gói tập active, progress bar, shortcuts |
| 13 | `gui/user/user_profile.py` | Thông tin cá nhân (read-only) + form đổi PIN |
| 14 | `gui/user/user_membership.py` | 2 tab: gói hiện tại + danh sách gói để đăng ký |
| 15 | `gui/user/user_history.py` | Bảng lịch sử gói tập, filter tháng/năm |
| 16 | `gui/user/user_notifications.py` | Danh sách thông báo, đánh dấu đã đọc |
| 17 | `gui/user/trainer_dashboard.py` | Dashboard HLV: thông tin + danh sách học viên |

### Files cần chỉnh sửa (2 files)
| STT | File | Thay đổi |
|-----|------|---------|
| 1 | `app/core/database.py` | Thêm bảng `trainers`, `notifications`; cột `pin` cho `members` |
| 2 | `app/services/trainer_svc.py` | Điền logic: register_trainer(), update_trainer(), get_trainer_members() |

---

## 8. KẾ HOẠCH TRIỂN KHAI

### Giai đoạn 1 — Nền tảng (Database & Models)
- Cập nhật `database.py`
- Tạo `trainer.py`, `notification.py`

### Giai đoạn 2 — Dữ liệu (Repositories & Services)
- Tạo `trainer_repo.py`, `notification_repo.py`
- Tạo `auth_svc.py`, `notification_svc.py`
- Cập nhật `trainer_svc.py`

### Giai đoạn 3 — Giao diện (GUI)
- `user_sidebar.py` → `user_login.py` → `user_dashboard.py`
- `user_profile.py` → `user_membership.py` → `user_history.py`
- `user_notifications.py` → `trainer_dashboard.py`

### Giai đoạn 4 — Tích hợp & Kiểm tra
- Tạo `user_main.py`
- Chạy `python app/user_main.py` kiểm tra từng màn hình
- Đảm bảo `python app/main.py` (admin) vẫn hoạt động bình thường

---

## 9. HƯỚNG DẪN CHẠY SAU KHI TRIỂN KHAI

```bash
# App Admin (hiện tại)
python app/main.py

# App Người dùng (mới)
python app/user_main.py
```

**Đăng nhập lần đầu:**
- PIN mặc định: `000000`
- Admin cần đặt SĐT cho hội viên trong app admin trước
- Hội viên đổi PIN sau khi đăng nhập lần đầu

---

*Báo cáo này mô tả kế hoạch thiết kế. Chờ duyệt trước khi bắt đầu triển khai code.*
