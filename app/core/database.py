# ============================================================================
# FILE: app/core/database.py
# MỤC ĐÍCH: Quản lý kết nối và khởi tạo database SQLite.
#            Cung cấp 2 thứ chính:
#              1. get_db()  — context manager để mở/đóng kết nối an toàn
#              2. init_db() — tạo các bảng (tables) nếu chưa tồn tại
# ============================================================================

import sqlite3                          # Thư viện SQLite có sẵn trong Python — database dạng file
from contextlib import contextmanager   # Decorator để tạo context manager (dùng với `with`)
from app.core.config import DB_PATH     # Đường dẫn tới file database (VD: data/gym_db.db)


@contextmanager  # ← Decorator biến hàm thành context manager (có thể dùng `with get_db() as conn:`)
def get_db():
    """Mở kết nối tới database và tự động đóng khi xong.

    Cách dùng:
        with get_db() as conn:
            conn.execute("SELECT * FROM members")
            # ... làm gì đó với database ...
        # ← Khi thoát khỏi `with`, kết nối tự động đóng

    Flow hoạt động:
        1. Mở kết nối tới file SQLite
        2. Bật foreign keys (ràng buộc khóa ngoại)
        3. `yield conn` — trả kết nối cho caller dùng
        4. Nếu KHÔNG có lỗi → commit (lưu thay đổi vào DB)
        5. Nếu CÓ lỗi → rollback (hủy thay đổi, quay về trạng thái trước)
        6. Cuối cùng (finally) → luôn đóng kết nối dù có lỗi hay không
    """
    # Bước 1: Mở kết nối tới file database
    conn = sqlite3.connect(DB_PATH)

    # Bước 2: Thiết lập row_factory = sqlite3.Row
    # → Khi query, kết quả trả về dạng dict-like (truy cập bằng tên cột)
    # VD: row["name"] thay vì row[1]
    conn.row_factory = sqlite3.Row

    # Bước 3: Bật ràng buộc khóa ngoại (foreign key)
    # SQLite mặc định TẮT foreign keys! Phải bật thủ công.
    # Khi bật: nếu insert subscription với member_id không tồn tại → sẽ báo lỗi
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        yield conn      # ← Trả kết nối cho caller (phần code trong `with`)
        conn.commit()   # ← Nếu không có lỗi → lưu thay đổi vào database
    except Exception:
        conn.rollback()  # ← Nếu có lỗi → hủy tất cả thay đổi chưa commit
        raise            # ← Ném lại lỗi để caller biết (không "nuốt" lỗi)
    finally:
        conn.close()     # ← LUÔN đóng kết nối, dù có lỗi hay không (tránh rò rỉ tài nguyên)


def init_db():
    """Tạo tất cả các bảng (tables) trong database nếu chưa tồn tại.

    Hàm này được gọi MỘT LẦN khi app khởi động (trong main.py).
    "CREATE TABLE IF NOT EXISTS" nghĩa là: chỉ tạo nếu bảng chưa có,
    nếu đã có rồi thì bỏ qua (không ghi đè dữ liệu cũ).

    LƯU Ý: Không dùng get_db() context manager ở đây vì executescript()
    tự commit ngầm — không tương thích với cơ chế commit/rollback của get_db().
    """
    # Mở kết nối trực tiếp (không qua get_db)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Bật foreign key

    try:
        # ── BẢNG 1: members (Hội viên) ───────────────────────────────────────
        # Lưu thông tin cá nhân của từng hội viên phòng gym
        conn.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id TEXT PRIMARY KEY,           -- UUID duy nhất cho mỗi hội viên (VD: "a1b2c3...")
                name TEXT NOT NULL,            -- Họ tên (bắt buộc, NOT NULL = không được để trống)
                phone TEXT NOT NULL,           -- Số điện thoại (bắt buộc)
                email TEXT,                    -- Email (tùy chọn, có thể NULL)
                gender TEXT,                   -- Giới tính: 'male', 'female', 'other'
                date_of_birth TEXT,            -- Ngày sinh dạng text (VD: "2000-01-15")
                address TEXT,                  -- Địa chỉ
                emergency_contact TEXT,        -- Số liên hệ khẩn cấp
                photo TEXT,                    -- Đường dẫn ảnh đại diện
                created_at TEXT NOT NULL,      -- Thời điểm tạo (ISO format: "2026-03-22T10:30:00")
                updated_at TEXT NOT NULL,      -- Thời điểm cập nhật gần nhất
                is_active INTEGER NOT NULL DEFAULT 1  -- 1 = đang hoạt động, 0 = đã xóa (soft delete)
            )
        """)

        # ── BẢNG 2: membership_plans (Gói tập) ───────────────────────────────
        # Định nghĩa các loại gói tập mà gym cung cấp (VD: Gói 1 tháng, 6 tháng, 1 năm)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS membership_plans (
                id TEXT PRIMARY KEY,           -- UUID duy nhất
                name TEXT NOT NULL,            -- Tên gói (VD: "Gói 1 tháng")
                duration_days INTEGER NOT NULL, -- Thời hạn tính bằng ngày (VD: 30, 180, 365)
                price REAL NOT NULL,           -- Giá gói (REAL = số thập phân, VD: 500000.0)
                description TEXT,              -- Mô tả chi tiết
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)

        # ── BẢNG 3: subscriptions (Đăng ký gói tập) ──────────────────────────
        # Lưu việc hội viên X đăng ký gói tập Y vào ngày nào, hết hạn khi nào
        # Đây là bảng LIÊN KẾT giữa members và membership_plans (quan hệ nhiều-nhiều)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                member_id TEXT NOT NULL,        -- ID hội viên (khóa ngoại → members.id)
                plan_id TEXT NOT NULL,           -- ID gói tập (khóa ngoại → membership_plans.id)
                price_paid REAL NOT NULL,        -- Số tiền thực tế đã thanh toán
                start_date TEXT NOT NULL,        -- Ngày bắt đầu gói tập
                end_date TEXT NOT NULL,          -- Ngày hết hạn gói tập
                status TEXT NOT NULL DEFAULT 'active',  -- Trạng thái: 'active', 'expired', 'cancelled'
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (member_id) REFERENCES members(id),          -- Ràng buộc: member_id phải tồn tại trong bảng members
                FOREIGN KEY (plan_id) REFERENCES membership_plans(id)    -- Ràng buộc: plan_id phải tồn tại trong bảng membership_plans
            )
        """)

        # ── BẢNG 4: equipment (Thiết bị) ─────────────────────────────────────
        # Quản lý máy móc, thiết bị trong phòng gym
        conn.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,             -- Tên thiết bị (VD: "Máy chạy bộ")
                category TEXT NOT NULL,         -- Phân loại (VD: "Cardio", "Tạ tự do")
                quantity INTEGER NOT NULL DEFAULT 1,  -- Số lượng
                status TEXT NOT NULL DEFAULT 'working',  -- 'working' | 'broken' | 'maintenance'
                purchase_date TEXT,             -- Ngày mua
                location TEXT,                  -- Vị trí (VD: "Tầng 1", "Khu Cardio")
                notes TEXT,                     -- Ghi chú bảo trì
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            )
        """)

        # ── INDEXES (Chỉ mục) ────────────────────────────────────────────────
        # Index giúp database TÌM KIẾM NHANH HƠN trên các cột hay query.
        # Giống như mục lục sách — thay vì đọc từng trang, tra mục lục sẽ nhanh hơn.
        # Trade-off: tốn thêm dung lượng lưu trữ, nhưng query nhanh hơn rất nhiều.
        conn.execute("CREATE INDEX IF NOT EXISTS idx_members_phone ON members(phone)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_members_is_active ON members(is_active)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_member_id ON subscriptions(member_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_plan_id ON subscriptions(plan_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_subs_status ON subscriptions(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_equipment_status ON equipment(status)")

        conn.commit()  # Lưu tất cả thay đổi vào database
    except Exception:
        conn.rollback()  # Có lỗi → hủy tất cả
        raise
    finally:
        conn.close()     # Luôn đóng kết nối
