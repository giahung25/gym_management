# ============================================================================
# FILE: app/core/config.py
# MỤC ĐÍCH: Lưu trữ các HẰNG SỐ CẤU HÌNH cho toàn bộ ứng dụng.
#            Các file khác sẽ import từ đây để dùng, giúp quản lý tập trung.
# ============================================================================

import os  # Thư viện chuẩn của Python — dùng để làm việc với file/thư mục/biến môi trường

# ── Đường dẫn thư mục gốc của dự án ──────────────────────────────────────────
# __file__         = đường dẫn tới file config.py (VD: E:/gym_management/app/core/config.py)
# abspath(__file__) = đường dẫn tuyệt đối (đầy đủ) của file này
# dirname()        = lấy thư mục cha. Gọi 3 lần để đi từ config.py → core/ → app/ → gym_management/
#   Lần 1: E:/gym_management/app/core/
#   Lần 2: E:/gym_management/app/
#   Lần 3: E:/gym_management/          ← đây là thư mục gốc dự án
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Đường dẫn tới file database SQLite ────────────────────────────────────────
# os.path.join() nối các phần đường dẫn lại: BASE_DIR + "data" + "gym_db.db"
# Kết quả VD: E:/gym_management/data/gym_db.db
DB_PATH = os.path.join(BASE_DIR, "data", "gym_db.db")

# ── Tiêu đề và kích thước cửa sổ ứng dụng ────────────────────────────────────
APP_TITLE = "GymAdmin Management System"  # Tên hiển thị trên thanh tiêu đề cửa sổ
WINDOW_WIDTH = 1280   # Chiều rộng cửa sổ tính bằng pixel
WINDOW_HEIGHT = 800   # Chiều cao cửa sổ tính bằng pixel

# ── Thông tin đăng nhập mặc định ──────────────────────────────────────────────
# os.environ.get("TÊN_BIẾN", "giá_trị_mặc_định"):
#   - Nếu biến môi trường "GYM_USERNAME" tồn tại → dùng giá trị đó
#   - Nếu KHÔNG tồn tại → dùng giá trị mặc định "admin"
# Cách này cho phép thay đổi username/password mà KHÔNG cần sửa code
ADMIN_USERNAME = os.environ.get("GYM_USERNAME", "admin")       # Mặc định: "admin"
ADMIN_PASSWORD = os.environ.get("GYM_PASSWORD", "admin123")    # Mặc định: "admin123"
